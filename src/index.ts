import express from 'express';
import cors from 'cors';
import pool from './config/database';
import userRoutes from './routes/userRoutes';

const app = express();
const PORT = process.env.PORT || 5002;

// CORS configuration
app.use(cors({
  origin: ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175', 
          'http://localhost:5176', 'http://localhost:5177', 'http://localhost:5178', 
          'http://localhost:5179', 'http://localhost:5180'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Middleware
app.use(express.json());

// Routes
app.use('/api/users', userRoutes);

// Test database connection
pool.getConnection()
  .then(connection => {
    console.log('Database connected successfully');
    connection.release();
  })
  .catch(error => {
    console.error('Error connecting to database:', error);
  });

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
}); 