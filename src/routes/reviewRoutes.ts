import express from 'express';
import { auth } from '../middleware/auth';
import {
  createReview,
  getProductReviews,
  getUserReviews,
  updateReview,
  deleteReview,
  markReviewHelpful
} from '../controllers/reviewController';

const router = express.Router();

// Get reviews for a specific product (public)
router.get('/product/:productId', getProductReviews);

// Get current user's reviews
router.get('/user', auth, getUserReviews);

// Create a new review
router.post('/', auth, createReview);

// Update a review
router.put('/:reviewId', auth, updateReview);

// Delete a review
router.delete('/:reviewId', auth, deleteReview);

// Mark review as helpful
router.post('/:reviewId/helpful', auth, markReviewHelpful);

export default router; 
