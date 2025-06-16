import { RowDataPacket } from 'mysql2';

export interface User extends RowDataPacket {
  id: string;
  username: string;
  email: string;
  password?: string;
  first_name?: string;
  last_name?: string;
  gender?: string;
  phone?: string;
  created_at?: Date;
  updated_at?: Date;
}

export interface UserUpdateData {
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  gender?: string;
  phone?: string;
}

export interface UserSignupData {
  username: string;
  email: string;
  password: string;
} 