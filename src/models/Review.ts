import { db } from '../config/database';

export interface Review {
  id?: number;
  user_id: string;
  product_id: number;
  rating: number;
  comment?: string;
  helpful_votes?: number;
  created_at?: Date;
  updated_at?: Date;
  user_name?: string;
  user_email?: string;
}

export interface ReviewWithUser extends Review {
  user_name: string;
  user_email: string;
}

export class ReviewModel {
  static async create(review: Omit<Review, 'id' | 'created_at' | 'updated_at'>): Promise<Review> {
    const [result] = await db.execute(
      'INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (?, ?, ?, ?)',
      [review.user_id, review.product_id, review.rating, review.comment]
    );
    
    const reviewId = (result as any).insertId;
    return this.findById(reviewId);
  }

  static async findById(id: number): Promise<Review | null> {
    const [rows] = await db.execute(
      'SELECT * FROM reviews WHERE id = ?',
      [id]
    );
    
    const reviews = rows as Review[];
    return reviews.length > 0 ? reviews[0] : null;
  }

  static async findByProductId(productId: number): Promise<ReviewWithUser[]> {
    const [rows] = await db.execute(`
      SELECT r.*, u.first_name, u.last_name, u.email 
      FROM reviews r 
      JOIN users u ON r.user_id = u.id 
      WHERE r.product_id = ? 
      ORDER BY r.created_at DESC
    `, [productId]);
    
    return (rows as any[]).map(row => ({
      ...row,
      user_name: `${row.first_name} ${row.last_name}`,
      user_email: row.email
    }));
  }

  static async findByUserId(userId: string): Promise<Review[]> {
    const [rows] = await db.execute(
      'SELECT * FROM reviews WHERE user_id = ? ORDER BY created_at DESC',
      [userId]
    );
    
    return rows as Review[];
  }

  static async update(id: number, review: Partial<Review>): Promise<Review | null> {
    const [result] = await db.execute(
      'UPDATE reviews SET rating = ?, comment = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [review.rating, review.comment, id]
    );
    
    if ((result as any).affectedRows > 0) {
      return this.findById(id);
    }
    return null;
  }

  static async delete(id: number): Promise<boolean> {
    const [result] = await db.execute(
      'DELETE FROM reviews WHERE id = ?',
      [id]
    );
    
    return (result as any).affectedRows > 0;
  }

  static async getProductRating(productId: number): Promise<{ average: number; count: number }> {
    const [rows] = await db.execute(
      'SELECT AVG(rating) as average, COUNT(*) as count FROM reviews WHERE product_id = ?',
      [productId]
    );
    
    const result = (rows as any[])[0];
    return {
      average: result.average ? parseFloat(result.average) : 0,
      count: result.count
    };
  }

  static async markHelpful(reviewId: number, userId: string): Promise<boolean> {
    try {
      // Check if user already voted
      const [existing] = await db.execute(
        'SELECT id FROM review_likes WHERE review_id = ? AND user_id = ?',
        [reviewId, userId]
      );
      
      if ((existing as any[]).length > 0) {
        // Remove existing vote
        await db.execute(
          'DELETE FROM review_likes WHERE review_id = ? AND user_id = ?',
          [reviewId, userId]
        );
        
        // Decrease helpful votes
        await db.execute(
          'UPDATE reviews SET helpful_votes = GREATEST(helpful_votes - 1, 0) WHERE id = ?',
          [reviewId]
        );
        
        return false; // Vote removed
      } else {
        // Add new vote
        await db.execute(
          'INSERT INTO review_likes (review_id, user_id) VALUES (?, ?)',
          [reviewId, userId]
        );
        
        // Increase helpful votes
        await db.execute(
          'UPDATE reviews SET helpful_votes = helpful_votes + 1 WHERE id = ?',
          [reviewId]
        );
        
        return true; // Vote added
      }
    } catch (error) {
      console.error('Error marking review as helpful:', error);
      return false;
    }
  }

  static async hasUserPurchasedProduct(userId: string, productId: number): Promise<boolean> {
    const [rows] = await db.execute(`
      SELECT COUNT(*) as count 
      FROM order_items oi 
      JOIN orders o ON oi.order_id = o.id 
      WHERE o.user_id = ? AND oi.product_id = ? AND o.status IN ('PAID', 'PROCESSING', 'SHIPPED', 'DELIVERED')
    `, [userId, productId]);
    
    return (rows as any[])[0].count > 0;
  }
} 
