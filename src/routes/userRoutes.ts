import express from 'express';
import { login, signup, getUserProfile, updateUserProfile, createUserProfile } from '../controllers/userController';
import { getUserAddresses, createAddress, updateAddress, deleteAddress } from '../controllers/addressController';
import { getUserOrders, getOrderDetails } from '../controllers/orderController';
import { auth } from '../middleware/auth';

const router = express.Router();

// Public routes
router.post('/login', login);
router.post('/signup', signup);

// Protected routes
router.get('/:id', auth, getUserProfile);
router.put('/:id', auth, updateUserProfile);
router.post('/', auth, createUserProfile);

// Address routes (protected)
router.get('/:userId/addresses', auth, getUserAddresses);
router.post('/:userId/addresses', auth, createAddress);
router.put('/:userId/addresses/:addressId', auth, updateAddress);
router.delete('/:userId/addresses/:addressId', auth, deleteAddress);

// Order routes (protected)
router.get('/:userId/orders', auth, getUserOrders);
router.get('/:userId/orders/:orderId', auth, getOrderDetails);

export default router;