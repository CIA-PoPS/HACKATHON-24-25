import express from 'express';
import cors from 'cors';
import userRoutes from './routes/userRoutes';
import codeRoutes from './routes/codeRoutes';
import dotenv from 'dotenv';

dotenv.config();

const app = express();

app.use(cors());

// app.use(cors({
//     origin: 'https://www.cia-pops.fr',
//     methods: 'GET, POST, PUT, DELETE',
//     allowedHeaders: 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
// }));

app.use(express.json());

app.use('/users', userRoutes);
app.use('/code' , codeRoutes);

app.listen(Number(process.env.PORT), () => {
    console.log('Server running on port ' + process.env.PORT);
});
