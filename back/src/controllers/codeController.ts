import { Request, Response } from 'express';
import { RowDataPacket, ResultSetHeader } from 'mysql2';
import { readFileSync, writeFileSync } from 'fs';
import { spawn } from 'child_process';
import { db } from '../config/database';
import { Submit } from '../models/codeModels';
import { User } from '../models/userModels';
import fs from "fs";
import { exec } from "child_process";
import { promisify } from "util";


export async function getSubmit(req: Request, res: Response): Promise<void> {
    const { userTMP } = req as any;

    if (userTMP === undefined) { res.status(403).json({ error: 'Not authenticated.' }); return; }

    try {
        let query: string = 'SELECT * FROM `users` WHERE `userId` = ?';
        let [result]: [RowDataPacket[], any] = await db.execute(query, [userTMP.id]);

        if (result.length === 0) { res.status(404).json({ error: 'User not found.' }); return; }

        const user: User = new User(result[0]);

        if (!user.isVerified || !user.isATeam) { res.status(403).json({ error: 'Not authorized.' }); return; }

        query = 'SELECT * FROM `submits` WHERE `teamId` = ?';
        [result] = await db.execute(query, [user.id]) as [RowDataPacket[], any];

        if (result.length === 0) { res.status(404).json({ error: 'Submit not found.' }); return; }

        const submit: Submit = new Submit(result[0]);

        res.status(200).json(submit);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching submit:\n' + error });
    }
}


export async function getFile(req: Request, res: Response): Promise<void> {
    const { extension } = req.params;
    const { userTMP } = req as any;

    if (userTMP === undefined) { res.status(403).json({ error: 'Not authenticated.' }); return; }

    try {
        let query: string = 'SELECT * FROM `users` WHERE `userId` = ?';
        let [result]: [RowDataPacket[], any] = await db.execute(query, [userTMP.id]);

        if (result.length === 0) { res.status(404).json({ error: 'User not found.' }); return; }

        const user: User = new User(result[0]);

        if (!user.isVerified || !user.isATeam) { res.status(403).json({ error: 'Not authorized.' }); return; }
        if (!user.isAdmin && extension === 'log') { res.status(403).json({ error: 'Not authorized.' }); return; }

        const filePath = `${process.env.SRC_FOLDER}/data/logs/${user.id}`;

        if (extension === 'zip') {
            const zipCommand = `zip -r ${filePath}.${extension} ${filePath}`;
            const execPromise = promisify(exec);
            try {
                await execPromise(zipCommand);
            } catch (error) {
                res.status(403).json({ error: "Failed to create zip" });
                return;
            }
        }

        if (!fs.existsSync(`${filePath}.${extension}`)) {
            res.status(404).json({ error: "File not found" });
            return;
        }

        res.download(`${filePath}.${extension}`, `hackathon-24-25.${extension}`, (err) => {
            if (err) {
                console.error("Download error:", err);
                if (!res.headersSent) {
                    res.status(500).json({ error: "Failed to download file" });
                }
            }
        });
    } catch (error) {
        console.error("Server error:", error);
        res.status(500).json({ error: "Error fetching file" });
    }
}


export async function getScoreboard(req: Request, res: Response): Promise<void> {
    try {
        const query: string = 'SELECT u.userNickname as team, s.submitScore FROM `submits` s JOIN `users` u ON s.teamId = u.userId';
        const [result]: [RowDataPacket[], any] = await db.execute(query);

        const scores: { team: string, score: number }[] = result.map(data => ({ team: data.team, score: data.submitScore }));

        res.status(200).json(scores);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching scoreboard:\n' + error });
    }
}


function checkIfError(teamId: number): boolean {
    const logContent: string = readFileSync(`${process.env.SRC_FOLDER}/data/logs/${teamId}.log`, 'utf8');
    return logContent !== '' && logContent !== '\n';
}


const lastSubmit: { teamId: number, time: Date }[] = [];


function callPythonScript(scriptPath: string, teamId: number, stages: number[]): Promise<{ canHaveError: boolean, scores: any }> {
    return new Promise<{ canHaveError: boolean, scores: number }>((resolve, reject) => {
        const pythonProcess = spawn('python3', [scriptPath, teamId.toString(), `${process.env.SRC_FOLDER}/data`, ...stages.map((x) => x.toString())]);

        let output: string = '';

        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.on('close', (code) => {
            const lastTime = lastSubmit.find((x) => x.teamId === teamId);
            if (lastTime === undefined) lastSubmit.push({ teamId, time: new Date() });
            else lastTime.time = new Date();
            if (code !== 0) reject(new Error());
            else resolve({ canHaveError: checkIfError(teamId), scores: JSON.parse(output) });
        });
    });
}

async function runSubmit(teamId: number, stages: number[]): Promise<void> {
    const query = 'UPDATE `submits` SET `submitStatus` = \'PENDING\' WHERE `teamId` = ?';
    db.execute(query, [teamId]);

    callPythonScript(`${process.env.SRC_FOLDER}/docker-run/runner.py`, teamId, stages)
        .then((res) => {
            console.log(res);
            const query = 'UPDATE `submits` SET `submitTime` = NOW(), `submitStatus` = \'FINISHED\', `submitCanHaveError` = ? WHERE `teamId` = ?';
            db.execute(query, [res.canHaveError, teamId]);
        })
        .catch((error) => {
            console.log(error);
            const query = 'UPDATE `submits` SET `submitTime` = NOW(), `submitStatus` = \'ERROR\', `submitCanHaveError` = ? WHERE `teamId` = ?';
            db.execute(query, [true, teamId]);
        });
}

const queue: { teamId: number, stages: number[], resolve: () => void }[] = [];
let activeJobs: number = 0;
const MAX_CONCURRENT_JOBS: number = 1;

async function processQueue(): Promise<void> {
    if (queue.length > 0 && activeJobs < MAX_CONCURRENT_JOBS) {
        const { teamId, stages, resolve } = queue.shift()!;
        activeJobs += 1;
        try {
            await runSubmit(teamId, stages);
            resolve();
        } finally {
            activeJobs -= 1;
            processQueue();
        }
    }
}

function addToQueue(teamId: number, stages: number[]): Promise<void> {
    return new Promise<void>((resolve) => {
        queue.push({ teamId, stages, resolve });
        processQueue();
    });
}


export async function postSubmit(req: Request, res: Response): Promise<void> {
    const { userTMP } = req as any;
    const { stages, code } = req.body;

    if (userTMP === undefined) { res.status(403).json({ error: 'Not authenticated.' }); return; }

    try {
        let query: string = 'SELECT * FROM `users` WHERE `userId` = ?';
        const [result]: [RowDataPacket[], any] = await db.execute(query, [userTMP.id]);

        if (result.length === 0) { res.status(404).json({ error: 'User not found.' }); return; }

        const user: User = new User(result[0]);

        const lastTime = lastSubmit.find((x) => x.teamId === user.id);
        if (lastTime !== undefined) {
            const timer: number = 5*60 - Math.ceil((new Date().getTime() - lastTime.time.getTime()) / 1000);
            if (!user.isAdmin && timer > 0) { res.status(403).json({ error: `Not authorized. You are in cooldown for ${timer}` }); return; }
        }

        query = 'UPDATE `submits` SET `submitStatus` = \'IN QUEUE\', `submitTime` = NOW(), `submitCanHaveError` = 0, `submitScore` = 0 WHERE `teamId` = ?';
        const [result2]: [ResultSetHeader, any] = await db.execute(query, [user.id]) as [ResultSetHeader, any];

        if (result2.affectedRows === 0) {
            query = 'INSERT INTO `submits` (`teamId`, `submitStatus`) VALUES (?, \'IN QUEUE\')';
            await db.execute(query, [user.id]);
        }

        writeFileSync(`${process.env.SRC_FOLDER}/data/tmp/${user.id}.py`, code);

        addToQueue(user.id, stages);

        res.status(200);
    } catch (error) {
        res.status(500).json({ error: 'Error creating submit :\n' + error });
    }
}
