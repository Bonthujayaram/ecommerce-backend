import express from 'express';
import { createOrder, getUserOrders, getOrderDetails } from '../controllers/orderController';
import { auth } from '../middleware/auth';

const router = express.Router();

// Protected routes
router.post('/', auth, createOrder);
router.get('/user/:userId', auth, getUserOrders);
router.get('/user/:userId/:orderId', auth, getOrderDetails);

export default router; 