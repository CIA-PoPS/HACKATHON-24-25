import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export function authenticateToken(req: Request, res: Response, next: NextFunction): void {
    const token = req.header('Authorization') || '';

    try {
        const user: any = jwt.verify(token, process.env.JWT_SECRET!);
        (req as any).userTMP = user;
        next();
    } catch (error) {
        (req as any).userTMP = undefined;
        next();
    }
}
