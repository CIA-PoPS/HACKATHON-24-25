import express from 'express';
import { getSubmit, getFile, getScoreboard, postSubmit } from '../controllers/codeController';
import { authenticateToken } from '../middlewares/authMiddleware';

const router = express.Router();

router.get( '/submits',       authenticateToken, getSubmit);
router.post('/submits',       authenticateToken, postSubmit);
router.get( '/dl/:extension', authenticateToken, getFile);
router.get( '/scoreboard',    getScoreboard);


export default router;
