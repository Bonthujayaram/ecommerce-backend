import { Request, Response } from 'express';
import pool from '../config/database';
import { Address, AddressCreateData } from '../models/Address';
import { ResultSetHeader } from 'mysql2';

// Get user addresses
export const getUserAddresses = async (req: Request, res: Response) => {
  const userId = req.params.userId;
  let connection;

  try {
    connection = await pool.getConnection();
    const [addresses] = await connection.execute<Address[]>(
      'SELECT * FROM addresses WHERE user_id = ?',
      [userId]
    );

    res.json(addresses);
  } catch (error) {
    console.error('Error fetching addresses:', error);
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

// Create address
export const createAddress = async (req: Request, res: Response) => {
  const userId = req.params.userId;
  const addressData: AddressCreateData = req.body;
  let connection;

  try {
    connection = await pool.getConnection();

    const [result] = await connection.execute<ResultSetHeader>(
      'INSERT INTO addresses (user_id, label, name, phone, address) VALUES (?, ?, ?, ?, ?)',
      [userId, addressData.label, addressData.name, addressData.phone, addressData.address]
    );

    const [newAddress] = await connection.execute<Address[]>(
      'SELECT * FROM addresses WHERE id = ?',
      [result.insertId]
    );

    res.status(201).json(newAddress[0]);
  } catch (error) {
    console.error('Error creating address:', error);
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

// Update address
export const updateAddress = async (req: Request, res: Response) => {
  const { userId, addressId } = req.params;
  const addressData: AddressCreateData = req.body;
  let connection;

  try {
    connection = await pool.getConnection();

    // Verify address belongs to user
    const [existingAddress] = await connection.execute<Address[]>(
      'SELECT id FROM addresses WHERE id = ? AND user_id = ?',
      [addressId, userId]
    );

    if (existingAddress.length === 0) {
      return res.status(404).json({ error: 'Address not found' });
    }

    await connection.execute<ResultSetHeader>(
      'UPDATE addresses SET label = ?, name = ?, phone = ?, address = ? WHERE id = ?',
      [addressData.label, addressData.name, addressData.phone, addressData.address, addressId]
    );

    const [updatedAddress] = await connection.execute<Address[]>(
      'SELECT * FROM addresses WHERE id = ?',
      [addressId]
    );

    res.json(updatedAddress[0]);
  } catch (error) {
    console.error('Error updating address:', error);
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

// Delete address
export const deleteAddress = async (req: Request, res: Response) => {
  const { userId, addressId } = req.params;
  let connection;

  try {
    connection = await pool.getConnection();

    // Verify address belongs to user
    const [existingAddress] = await connection.execute<Address[]>(
      'SELECT id FROM addresses WHERE id = ? AND user_id = ?',
      [addressId, userId]
    );

    if (existingAddress.length === 0) {
      return res.status(404).json({ error: 'Address not found' });
    }

    await connection.execute<ResultSetHeader>(
      'DELETE FROM addresses WHERE id = ?',
      [addressId]
    );

    res.status(204).send();
  } catch (error) {
    console.error('Error deleting address:', error);
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