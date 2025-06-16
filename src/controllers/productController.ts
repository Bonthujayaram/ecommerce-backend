import { Request, Response } from 'express';
import { pool } from '../config/db';
import { Product } from '../models/Product';
import { ResultSetHeader, RowDataPacket } from 'mysql2';

export const getAllProducts = async (req: Request, res: Response) => {
  try {
    console.log('Attempting to fetch all products...');
    const [rows] = await pool.execute('SELECT * FROM product');
    console.log('Products fetched successfully:', rows);
    res.json(rows);
  } catch (error) {
    console.error('Error in getAllProducts:', error);
    res.status(500).json({ 
      message: 'Error fetching products',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

export const searchProducts = async (req: Request, res: Response) => {
  try {
    const searchTerm = req.query.q as string;
    if (!searchTerm) {
      return res.status(400).json({ message: 'Search term is required' });
    }

    const [products] = await pool.execute<Product[]>(
      'SELECT * FROM product WHERE name LIKE ? OR description LIKE ?',
      [`%${searchTerm}%`, `%${searchTerm}%`]
    );
    res.json(products);
  } catch (error) {
    console.error('Error in searchProducts:', error);
    res.status(500).json({ 
      message: 'Error searching products',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

export const getProductsByCategory = async (req: Request, res: Response) => {
  try {
    const category = req.params.category;
    const [products] = await pool.execute<Product[]>(
      'SELECT * FROM product WHERE category = ?',
      [category]
    );
    res.json(products);
  } catch (error) {
    console.error('Error in getProductsByCategory:', error);
    res.status(500).json({ 
      message: 'Error fetching products by category',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}; 