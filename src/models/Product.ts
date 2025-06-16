import { RowDataPacket } from 'mysql2';

export interface Product extends RowDataPacket {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  image_url: string;
  stock: number;
  rating?: number;
  created_at?: Date;
  updated_at?: Date;
}

export interface ProductCreateData {
  name: string;
  description: string;
  price: number;
  category: string;
  image_url: string;
  stock: number;
  rating?: number;
}

export interface ProductUpdateData {
  name?: string;
  description?: string;
  price?: number;
  category?: string;
  image_url?: string;
  stock?: number;
  rating?: number;
} 