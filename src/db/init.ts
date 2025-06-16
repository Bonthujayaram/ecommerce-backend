import { pool } from '../config/db';
import fs from 'fs';
import path from 'path';

async function initDatabase() {
  let connection;
  try {
    connection = await pool.getConnection();
    console.log('Connected to database');

    // Read schema file
    const schemaPath = path.join(__dirname, 'schema.sql');
    const schema = fs.readFileSync(schemaPath, 'utf8');

    // Split schema into individual statements
    const statements = schema
      .split(';')
      .map(statement => statement.trim())
      .filter(statement => statement.length > 0);

    // Execute each statement
    for (const statement of statements) {
      try {
        await connection.execute(statement + ';');
        console.log('Executed statement:', statement.substring(0, 50) + '...');
      } catch (error) {
        console.error('Error executing statement:', statement);
        console.error('Error details:', error);
      }
    }

    console.log('Database initialization completed');
  } catch (error) {
    console.error('Database initialization failed:', error);
  } finally {
    if (connection) {
      connection.release();
      console.log('Database connection released');
    }
  }
}

// Run initialization
initDatabase().then(() => {
  console.log('Database initialization script completed');
  process.exit(0);
}).catch(error => {
  console.error('Database initialization script failed:', error);
  process.exit(1);
}); 