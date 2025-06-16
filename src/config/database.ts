import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();

const pool = mysql.createPool({
  host: process.env.DB_HOST ,
  user: process.env.DB_USER ,
  password: process.env.DB_PASSWORD ,
  database: process.env.DB_NAME ,
  port: parseInt(process.env.DB_PORT ?? (() => { throw new Error('DB_PORT is required') })()),
  ssl: {
    rejectUnauthorized: false // For development only - in production, you should use proper SSL
  },
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Test the database connection
const testConnection = async () => {
  try {
    const connection = await pool.getConnection();
    console.log('Database connected successfully');
    
    // Test if we can query the database
    const [rows] = await connection.query('SELECT 1 as test');
    console.log('Database query successful:', rows);
    
    connection.release();
    return true;
  } catch (err) {
    console.error('Database connection error:', err);
    return false;
  }
};

// Initial connection test
testConnection();

export default pool; 