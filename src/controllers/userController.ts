import { Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { pool } from '../config/db';
import { User, UserUpdateData } from '../models/User';
import { ResultSetHeader } from 'mysql2';
import { UserSignupData } from '../types/user';

// Get user profile
export const getUserProfile = async (req: Request, res: Response) => {
  const userId = req.params.id;
  let connection;
  
  try {
    console.log('Getting user profile for ID:', userId);
    
    connection = await pool.getConnection();
    console.log('Database connection established');

    const query = 'SELECT id, username, email, first_name, last_name, gender, phone FROM users WHERE id = ?';
    console.log('Executing query:', query, 'with params:', [userId]);

    const [rows] = await connection.execute<User[]>(query, [userId]);
    console.log('Query result:', rows);

    if (rows.length === 0) {
      console.log('No user found with ID:', userId);
      return res.status(404).json({ error: 'User not found' });
    }

    console.log('User found:', rows[0]);
    res.json(rows[0]);
  } catch (error) {
    console.error('Error fetching user profile:', error);
    console.error('Error details:', {
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined,
      userId
    });
    res.status(500).json({ 
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  } finally {
    if (connection) {
      try {
        await connection.release();
        console.log('Database connection released');
      } catch (releaseError) {
        console.error('Error releasing connection:', releaseError);
      }
    }
  }
};

// Update user profile
export const updateUserProfile = async (req: Request, res: Response) => {
  const userId = req.params.id;
  const updateData: UserUpdateData = req.body;
  let connection;
  
  try {
    connection = await pool.getConnection();

    // Validate if user exists
    const [existingUser] = await connection.execute<User[]>(
      'SELECT id FROM users WHERE id = ?',
      [userId]
    );

    if (existingUser.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Build update query dynamically based on provided fields
    const updateFields: string[] = [];
    const values: any[] = [];
    
    Object.entries(updateData).forEach(([key, value]) => {
      if (value !== undefined) {
        updateFields.push(`${key} = ?`);
        values.push(value);
      }
    });

    if (updateFields.length === 0) {
      return res.status(400).json({ error: 'No valid fields to update' });
    }

    values.push(userId);

    const query = `
      UPDATE users 
      SET ${updateFields.join(', ')}
      WHERE id = ?
    `;

    await connection.execute<ResultSetHeader>(query, values);

    // Fetch updated user data
    const [updatedUser] = await connection.execute<User[]>(
      'SELECT id, username, email, first_name, last_name, gender, phone FROM users WHERE id = ?',
      [userId]
    );

    res.json(updatedUser[0]);
  } catch (error) {
    console.error('Error updating user profile:', error);
    res.status(500).json({ 
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  } finally {
    if (connection) {
      connection.release();
    }
  }
};

// Create new user profile
export const createUserProfile = async (req: Request, res: Response) => {
  const { first_name, last_name, gender, email, phone } = req.body;
  let connection;

  try {
    connection = await pool.getConnection();
    const id = uuidv4();

    await connection.execute<ResultSetHeader>(
      'INSERT INTO users (id, first_name, last_name, gender, email, phone) VALUES (?, ?, ?, ?, ?, ?)',
      [id, first_name, last_name, gender, email, phone]
    );

    const [newUser] = await connection.execute<User[]>(
      'SELECT id, username, email, first_name, last_name, gender, phone FROM users WHERE id = ?',
      [id]
    );

    res.status(201).json(newUser[0]);
  } catch (error) {
    console.error('Error creating user profile:', error);
    res.status(500).json({ 
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  } finally {
    if (connection) {
      connection.release();
    }
  }
};

export const login = async (req: Request, res: Response) => {
  let connection;
  try {
    const { email, password } = req.body;
    console.log('Login attempt for email:', email);
    console.log('Received password:', password);

    // Input validation
    if (!email || !password) {
      console.log('Missing email or password');
      return res.status(400).json({ error: 'Email and password are required' });
    }

    // Get connection from pool
    connection = await pool.getConnection();
    console.log('Database connection established');

    // Find user by email
    const [users] = await connection.query<any[]>(
      'SELECT * FROM users WHERE email = ?',
      [email]
    );
    console.log('User query completed, found:', users.length > 0);

    const user = users[0];

    if (!user) {
      console.log('No user found with email:', email);
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    console.log('Found user:', { id: user.id, email: user.email, username: user.username });
    console.log('Stored hashed password:', user.password);

    // Compare password
    console.log('Comparing passwords...');
    const isValidPassword = await bcrypt.compare(password, user.password);
    console.log('Password comparison result:', isValidPassword);

    if (!isValidPassword) {
      console.log('Invalid password for user:', email);
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    // Generate JWT token
    const token = jwt.sign(
      { id: user.id, email: user.email },
      process.env.JWT_SECRET || 'your-secret-key',
      { expiresIn: '24h' }
    );
    console.log('Generated token for user:', user.id);

    // Send user data and token
    console.log('Login successful for user:', user.username);
    res.status(200).json({
      message: 'Login successful',
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    console.error('Error details:', {
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined
    });
    res.status(500).json({ 
      error: 'Internal server error', 
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  } finally {
    if (connection) {
      connection.release();
      console.log('Database connection released');
    }
  }
};

export const signup = async (req: Request, res: Response) => {
  let connection;
  try {
    const { username, email, password }: UserSignupData = req.body;

    // Input validation
    if (!username || !email || !password) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    connection = await pool.getConnection();

    // Check if user already exists
    const [existingUsers] = await connection.query<any[]>(
      'SELECT id FROM users WHERE email = ?',
      [email]
    );

    if (existingUsers.length > 0) {
      return res.status(400).json({ error: 'Email already registered' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
    const userId = uuidv4();

    // Create user
    await connection.execute<ResultSetHeader>(
      'INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)',
      [userId, username, email, hashedPassword]
    );

    // Generate token
    const token = jwt.sign(
      { id: userId, email },
      process.env.JWT_SECRET || 'your-secret-key',
      { expiresIn: '24h' }
    );

    res.status(201).json({
      message: 'User created successfully',
      token,
      user: {
        id: userId,
        username,
        email
      }
    });
  } catch (error) {
    console.error('Signup error:', error);
    res.status(500).json({ 
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  } finally {
    if (connection) {
      connection.release();
    }
  }
}; 