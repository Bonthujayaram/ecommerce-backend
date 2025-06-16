import { pool } from '../config/db';
import fs from 'fs';
import path from 'path';

async function runMigration() {
  let connection;
  try {
    connection = await pool.getConnection();
    console.log('Database connected successfully');
    
    // Read the migration file from src directory
    const migrationPath = path.join(__dirname, '..', '..', 'src', 'db', 'migrations', '004_fix_orders_table.sql');
    const migration = fs.readFileSync(migrationPath, 'utf8');

    // Split into individual statements
    const statements = migration.split(';').filter(stmt => stmt.trim());

    // Execute each statement
    for (const statement of statements) {
      if (statement.trim()) {
        try {
          await connection.execute(statement);
          console.log('Executed:', statement.trim().slice(0, 50) + '...');
        } catch (error) {
          console.error('Error executing statement:', error);
          throw error;
        }
      }
    }

    console.log('Migration completed successfully');
  } catch (error) {
    console.error('Error running migration:', error);
    throw error;
  } finally {
    if (connection) {
      connection.release();
    }
  }
}

runMigration().catch(console.error); 