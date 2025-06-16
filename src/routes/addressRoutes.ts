import express from 'express';
import { getUserAddresses, createAddress, updateAddress, deleteAddress } from '../controllers/addressController';
import { auth } from '../middleware/auth';

const router = express.Router();

// All address routes are protected
router.get('/:userId/addresses', auth, getUserAddresses);
router.post('/:userId/addresses', auth, createAddress);
router.put('/:userId/addresses/:addressId', auth, updateAddress);
router.delete('/:userId/addresses/:addressId', auth, deleteAddress);

export default router; 