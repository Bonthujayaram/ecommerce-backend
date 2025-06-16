import express from 'express';
import { getAllProducts, searchProducts, getProductsByCategory } from '../controllers/productController';

const router = express.Router();

// Get all products
router.get('/', getAllProducts);

// Search products
router.get('/search', searchProducts);

// Get products by category
router.get('/category/:category', getProductsByCategory);

export default router; 