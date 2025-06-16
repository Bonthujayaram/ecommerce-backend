import { RowDataPacket } from 'mysql2';

export interface Order extends RowDataPacket {
  id: number;
  user_id: string;
  address_id: number;
  total_amount: number;
  payment_method: 'UPI' | 'QR';
  payment_details: string;
  status: string;
  created_at?: Date;
  updated_at?: Date;
}

export interface OrderItem extends RowDataPacket {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  price: number;
  created_at?: Date;
  updated_at?: Date;
}

export interface OrderCreateData {
  user_id: string;
  total_amount: number;
  payment_method: 'UPI' | 'QR';
  payment_details: string;
  status: string;
  address_id: number;
  order_items: Array<{
    product_id: number;
    quantity: number;
    price: number;
  }>;
} 