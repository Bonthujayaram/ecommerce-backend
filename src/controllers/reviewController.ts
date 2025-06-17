import { Request, Response } from 'express';
import { ReviewModel, Review } from '../models/Review';
import { auth } from '../middleware/auth';

export const createReview = async (req: Request, res: Response) => {
  try {
    const { product_id, rating, comment } = req.body;
    const user_id = (req as any).user.id;

    // Validate input
    if (!product_id || !rating || rating < 1 || rating > 5) {
      return res.status(400).json({ 
        error: 'Invalid input. Product ID and rating (1-5) are required.' 
      });
    }

    // Check if user has already reviewed this product
    const existingReviews = await ReviewModel.findByUserId(user_id);
    const hasReviewed = existingReviews.some(review => review.product_id === product_id);
    
    if (hasReviewed) {
      return res.status(400).json({ 
        error: 'You have already reviewed this product.' 
      });
    }

    // Optional: Check if user has purchased the product (for verified purchase badge)
    const hasPurchased = await ReviewModel.hasUserPurchasedProduct(user_id, product_id);

    const review = await ReviewModel.create({
      user_id,
      product_id,
      rating,
      comment: comment || null
    });

    // Update product's average rating
    const productRating = await ReviewModel.getProductRating(product_id);
    
    res.status(201).json({
      message: 'Review created successfully',
      review: {
        ...review,
        verified_purchase: hasPurchased
      },
      product_rating: productRating
    });
  } catch (error) {
    console.error('Error creating review:', error);
    res.status(500).json({ error: 'Failed to create review' });
  }
};

export const getProductReviews = async (req: Request, res: Response) => {
  try {
    const { productId } = req.params;
    const product_id = parseInt(productId);

    if (isNaN(product_id)) {
      return res.status(400).json({ error: 'Invalid product ID' });
    }

    const reviews = await ReviewModel.findByProductId(product_id);
    const ratingStats = await ReviewModel.getProductRating(product_id);

    res.json({
      reviews,
      rating_stats: ratingStats
    });
  } catch (error) {
    console.error('Error fetching reviews:', error);
    res.status(500).json({ error: 'Failed to fetch reviews' });
  }
};

export const getUserReviews = async (req: Request, res: Response) => {
  try {
    const user_id = (req as any).user.id;
    const reviews = await ReviewModel.findByUserId(user_id);

    res.json({ reviews });
  } catch (error) {
    console.error('Error fetching user reviews:', error);
    res.status(500).json({ error: 'Failed to fetch user reviews' });
  }
};

export const updateReview = async (req: Request, res: Response) => {
  try {
    const { reviewId } = req.params;
    const { rating, comment } = req.body;
    const user_id = (req as any).user.id;

    const reviewIdNum = parseInt(reviewId);
    if (isNaN(reviewIdNum)) {
      return res.status(400).json({ error: 'Invalid review ID' });
    }

    // Get the review to check ownership
    const existingReview = await ReviewModel.findById(reviewIdNum);
    if (!existingReview) {
      return res.status(404).json({ error: 'Review not found' });
    }

    if (existingReview.user_id !== user_id) {
      return res.status(403).json({ error: 'You can only update your own reviews' });
    }

    // Validate rating
    if (rating && (rating < 1 || rating > 5)) {
      return res.status(400).json({ error: 'Rating must be between 1 and 5' });
    }

    const updatedReview = await ReviewModel.update(reviewIdNum, { rating, comment });
    
    if (!updatedReview) {
      return res.status(500).json({ error: 'Failed to update review' });
    }

    // Update product's average rating
    const productRating = await ReviewModel.getProductRating(existingReview.product_id);

    res.json({
      message: 'Review updated successfully',
      review: updatedReview,
      product_rating: productRating
    });
  } catch (error) {
    console.error('Error updating review:', error);
    res.status(500).json({ error: 'Failed to update review' });
  }
};

export const deleteReview = async (req: Request, res: Response) => {
  try {
    const { reviewId } = req.params;
    const user_id = (req as any).user.id;

    const reviewIdNum = parseInt(reviewId);
    if (isNaN(reviewIdNum)) {
      return res.status(400).json({ error: 'Invalid review ID' });
    }

    // Get the review to check ownership
    const existingReview = await ReviewModel.findById(reviewIdNum);
    if (!existingReview) {
      return res.status(404).json({ error: 'Review not found' });
    }

    if (existingReview.user_id !== user_id) {
      return res.status(403).json({ error: 'You can only delete your own reviews' });
    }

    const success = await ReviewModel.delete(reviewIdNum);
    
    if (!success) {
      return res.status(500).json({ error: 'Failed to delete review' });
    }

    // Update product's average rating
    const productRating = await ReviewModel.getProductRating(existingReview.product_id);

    res.json({
      message: 'Review deleted successfully',
      product_rating: productRating
    });
  } catch (error) {
    console.error('Error deleting review:', error);
    res.status(500).json({ error: 'Failed to delete review' });
  }
};

export const markReviewHelpful = async (req: Request, res: Response) => {
  try {
    const { reviewId } = req.params;
    const user_id = (req as any).user.id;

    const reviewIdNum = parseInt(reviewId);
    if (isNaN(reviewIdNum)) {
      return res.status(400).json({ error: 'Invalid review ID' });
    }

    const isHelpful = await ReviewModel.markHelpful(reviewIdNum, user_id);
    
    res.json({
      message: isHelpful ? 'Review marked as helpful' : 'Helpful vote removed',
      is_helpful: isHelpful
    });
  } catch (error) {
    console.error('Error marking review as helpful:', error);
    res.status(500).json({ error: 'Failed to mark review as helpful' });
  }
}; 
