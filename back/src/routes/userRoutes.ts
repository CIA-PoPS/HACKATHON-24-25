import express from 'express';
import { registerUser, verifyEmail, getUser } from '../controllers/userController';
import { loginUser } from '../controllers/authController';
import { authenticateToken } from '../middlewares/authMiddleware';

const router = express.Router();

router.post('/register'     , registerUser);
router.get( '/verify/:token', verifyEmail);
router.post('/login'        , loginUser);
router.get( '/get'          , authenticateToken, getUser);

export default router;
