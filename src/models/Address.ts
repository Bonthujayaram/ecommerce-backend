import { RowDataPacket } from 'mysql2';

export interface Address extends RowDataPacket {
  id: number;
  user_id: string;
  label: string;
  name: string;
  phone: string;
  address: string;
  created_at?: Date;
  updated_at?: Date;
}

export interface AddressCreateData {
  label: string;
  name: string;
  phone: string;
  address: string;
} 