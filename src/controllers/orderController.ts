import { Request, Response } from 'express';
import { pool } from '../config/db';
import { Order, OrderItem, OrderCreateData } from '../models/Order';
import { ResultSetHeader, PoolConnection } from 'mysql2/promise';

// Get user orders
export const getUserOrders = async (req: Request, res: Response) => {
  const userId = req.params.userId;
  let connection: PoolConnection | null = null;

  try {
    connection = await pool.getConnection();
    console.log('Getting orders for user:', userId);

    // Get all orders for the user
    const [orders] = await connection.execute<Order[]>(
      'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC',
      [userId]
    );

    // Get order items for each order
    const ordersWithItems = await Promise.all(orders.map(async (order) => {
      const [items] = await connection!.execute<OrderItem[]>(
        'SELECT * FROM order_items WHERE order_id = ?',
        [order.id]
      );
      return { 
        ...order, 
        order_date: order.created_at,
        items 
      };
    }));

    res.json(ordersWithItems);
  } catch (error) {
    console.error('Error fetching user orders:', error);
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

// Get order details
export const getOrderDetails = async (req: Request, res: Response) => {
  const { userId, orderId } = req.params;
  let connection: PoolConnection | null = null;

  try {
    connection = await pool.getConnection();
    console.log('Getting order details:', { userId, orderId });

    // Get the order
    const [orders] = await connection.execute<Order[]>(
      'SELECT * FROM orders WHERE id = ? AND user_id = ?',
      [orderId, userId]
    );

    if (orders.length === 0) {
      return res.status(404).json({ error: 'Order not found' });
    }

    // Get order items
    const [items] = await connection.execute<OrderItem[]>(
      'SELECT oi.*, p.name as product_name, p.description as product_description, p.image_url as product_image FROM order_items oi LEFT JOIN product p ON oi.product_id = p.id WHERE oi.order_id = ?',
      [orderId]
    );

    // Get address details
    const [addresses] = await connection.execute<any[]>(
      'SELECT * FROM addresses WHERE id = ?',
      [orders[0].address_id]
    );

    res.json({
      ...orders[0],
      items,
      address: addresses[0]
    });
  } catch (error) {
    console.error('Error fetching order details:', error);
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

// Create order
export const createOrder = async (req: Request, res: Response) => {
  const orderData: OrderCreateData = req.body;
  let connection;

  try {
    // Log the incoming order data
    console.log('Received order data:', JSON.stringify(orderData, null, 2));

    // Validate required fields
    if (!orderData.user_id) {
      return res.status(400).json({ error: 'user_id is required' });
    }
    if (!orderData.address_id) {
      return res.status(400).json({ error: 'address_id is required' });
    }
    if (!orderData.total_amount || orderData.total_amount <= 0) {
      return res.status(400).json({ error: 'valid total_amount is required' });
    }
    if (!orderData.payment_method) {
      return res.status(400).json({ error: 'payment_method is required' });
    }
    if (!orderData.status) {
      return res.status(400).json({ error: 'status is required' });
    }
    if (!orderData.order_items || !Array.isArray(orderData.order_items) || orderData.order_items.length === 0) {
      return res.status(400).json({ error: 'order_items must be a non-empty array' });
    }

    // Validate each order item
    for (const item of orderData.order_items) {
      if (!item.product_id) {
        return res.status(400).json({ error: 'product_id is required for each order item' });
      }
      if (!item.quantity || item.quantity <= 0) {
        return res.status(400).json({ error: 'valid quantity is required for each order item' });
      }
      if (!item.price || item.price <= 0) {
        return res.status(400).json({ error: 'valid price is required for each order item' });
      }
    }

    try {
      connection = await pool.getConnection();
      console.log('Database connection established');
    } catch (dbError) {
      console.error('Failed to get database connection:', dbError);
      return res.status(500).json({ 
        error: 'Database connection failed',
        details: dbError instanceof Error ? dbError.message : 'Unknown error'
      });
    }
    
    try {
      await connection.beginTransaction();
      console.log('Transaction started');

      // Verify user exists
      const [users] = await connection.execute<any[]>(
        'SELECT id FROM users WHERE id = ?',
        [orderData.user_id]
      );
      console.log('User check result:', users);
      
      if (users.length === 0) {
        await connection.rollback();
        return res.status(404).json({ error: 'User not found' });
      }

      // Verify address exists and belongs to user
      const [addresses] = await connection.execute<any[]>(
        'SELECT id FROM addresses WHERE id = ? AND user_id = ?',
        [orderData.address_id, orderData.user_id]
      );
      console.log('Address check result:', addresses);
      
      if (addresses.length === 0) {
        await connection.rollback();
        return res.status(404).json({ error: 'Address not found or does not belong to user' });
      }

      // Verify all products exist and check prices
      for (const item of orderData.order_items) {
        const [products] = await connection.execute<any[]>(
          'SELECT id, price FROM product WHERE id = ?',
          [item.product_id]
        );
        console.log(`Product check result for ${item.product_id}:`, products);
        
        if (products.length === 0) {
          await connection.rollback();
          return res.status(404).json({ error: `Product not found: ${item.product_id}` });
        }
        
        const product = products[0];
        if (Math.abs(product.price - item.price) > 0.01) {
          await connection.rollback();
          return res.status(400).json({ 
            error: `Price mismatch for product ${item.product_id}. Expected: ${product.price}, Got: ${item.price}` 
          });
        }
      }

      // Create order
      console.log('Creating order with data:', {
        user_id: orderData.user_id,
        address_id: orderData.address_id,
        total_amount: orderData.total_amount,
        payment_method: orderData.payment_method,
        payment_details: orderData.payment_details,
        status: orderData.status
      });

      const [orderResult] = await connection.execute<ResultSetHeader>(
        'INSERT INTO orders (user_id, address_id, total_amount, payment_method, payment_details, status) VALUES (?, ?, ?, ?, ?, ?)',
        [
          orderData.user_id,
          orderData.address_id,
          orderData.total_amount,
          orderData.payment_method,
          orderData.payment_details,
          orderData.status
        ]
      );
      console.log('Order created with ID:', orderResult.insertId);

      const orderId = orderResult.insertId;

      // Create order items
      for (const item of orderData.order_items) {
        console.log('Creating order item:', JSON.stringify(item, null, 2));
        try {
          await connection.execute<ResultSetHeader>(
            'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
            [orderId, item.product_id, item.quantity, item.price]
          );
        } catch (itemError) {
          console.error('Error creating order item:', itemError);
          await connection.rollback();
          return res.status(500).json({ 
            error: 'Failed to create order item',
            details: itemError instanceof Error ? itemError.message : 'Unknown error'
          });
        }
      }
      console.log('All order items created');

      await connection.commit();
      console.log('Transaction committed');

      // Fetch the created order with its items
      const [orders] = await connection.execute<Order[]>(
        'SELECT * FROM orders WHERE id = ?',
        [orderId]
      );
      console.log('Fetched order:', JSON.stringify(orders[0], null, 2));

      const [orderItems] = await connection.execute<OrderItem[]>(
        'SELECT * FROM order_items WHERE order_id = ?',
        [orderId]
      );
      console.log('Fetched order items:', JSON.stringify(orderItems, null, 2));

      res.status(201).json({
        ...orders[0],
        items: orderItems
      });
    } catch (txError) {
      if (connection) {
        await connection.rollback();
        console.log('Transaction rolled back due to error:', txError);
      }
      throw txError; // Re-throw to be caught by outer catch
    }
  } catch (error) {
    console.error('Error creating order:', error);
    console.error('Error details:', {
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined,
      orderData: JSON.stringify(orderData, null, 2)
    });

    // Check for specific MySQL errors
    if (error instanceof Error && error.message.includes('ER_NO_REFERENCED_ROW')) {
      return res.status(400).json({
        error: 'Invalid reference',
        details: 'One or more referenced IDs (user, address, or product) do not exist'
      });
    }

    if (error instanceof Error && error.message.includes('ER_DUP_ENTRY')) {
      return res.status(400).json({
        error: 'Duplicate entry',
        details: 'An order with these details already exists'
      });
    }

    res.status(500).json({
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error',
      message: 'Failed to create order. Please try again.'
    });
  } finally {
    if (connection) {
      connection.release();
      console.log('Database connection released');
    }
  }
}; 