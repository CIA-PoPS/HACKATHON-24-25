import { Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { db } from '../config/database';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';
import { RowDataPacket } from 'mysql2';
import { User } from '../models/userModels';

dotenv.config();

const transporter = nodemailer.createTransport({
    host:   process.env.MAIL_HOST,
    port:   Number(process.env.MAIL_PORT),
    secure: true,
    auth: {
        user: process.env.MAIL_USER,
        pass: process.env.MAIL_PASSWORD
    }
});

export async function registerUser(req: Request, res: Response): Promise<void> {
    const { email, nickname, password } = req.body;

    const hashedPassword   : any = await bcrypt.hash(password, 10);
    const verificationToken: any = jwt.sign({ email }, process.env.JWT_SECRET!, { expiresIn: '1h' });

    try {
        await db.execute(
            'INSERT INTO `users` (`userEmail`, `userNickname`, `userPassword`) VALUES (?, ?, ?)', 
            [email, nickname, hashedPassword]
        );

        const verificationLink: string = `${process.env.BACK_URL}/users/verify/${verificationToken}`;
        await transporter.sendMail({
            from:    process.env.MAIL_USER,
            to:      email,
            subject: 'Verify Your Email',
            text:    `Click this link to verify your email: ${verificationLink}. This link will expire in 1 hour.`
        });

        res.status(200).json({ message: 'User registered, please verify your email.' });
    } catch (error) {
        res.status(500).json({ error: 'Error registering user :\n' + error });
    }
}

export async function verifyEmail(req: Request, res: Response): Promise<void> {
    const { token } = req.params;

    try {
        const { email } = jwt.verify(token, process.env.JWT_SECRET!) as { email: string };

        await db.execute('UPDATE `users` SET `userIsVerified` = true WHERE `userEmail` = ?', [email]);

        res.status(200).json({ message: 'Email verified successfully.' });
    } catch (error) {
        res.status(400).json({ error: 'Invalid or expired token :\n' + error });
    }
}

export async function getUser(req: Request, res: Response): Promise<void> {
    const { userTMP } = req as any;

    if (userTMP === undefined) { res.status(403).json({ error: 'Not authenticated.' }); return; }

    try {
        const query   : string          = 'SELECT * FROM `users` WHERE `userId` = ?';
        const [result]: [RowDataPacket[], any] = await db.execute(query, [userTMP.id]);

        if (result.length === 0) { res.status(404).json({ error: 'User not found.' }); return; }

        const logedAs: User = new User(result[0]);
        logedAs.password = '';

        res.status(200).json(logedAs);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching user :\n' + error });
    }
}
