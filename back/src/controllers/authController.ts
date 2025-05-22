import { Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { RowDataPacket } from 'mysql2';
import { db } from '../config/database';
import { User } from '../models/userModels';

export async function loginUser(req: Request, res: Response): Promise<void> {
    const { email, nickname, password } = req.body;

    try {
        const [rows]: [RowDataPacket[], any] = await db.execute('SELECT * FROM `users` WHERE `userEmail` = ? OR `userNickname` = ?', [email, nickname]);

        if (rows.length === 0) { res.status(404).json({ error: 'User not found.' }); return; }

        const user: User = new User(rows[0]);
        if (!user.isVerified) { res.status(403).json({ error: 'Email not verified.' }); return; }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) { res.status(403).json({ error: 'Invalid credentials.' }); return; }

        const token = jwt.sign({ id: user.id, isAdmin: user.isAdmin }, process.env.JWT_SECRET!, { expiresIn: '6h' });

        res.status(200).json({ token });
    } catch (error) {
        res.status(500).json({ error: 'Error logging in user :\n' + error });
    }
}
