export interface User {
  id: string;
  username: string;
  email: string;
  password: string;
  created_at: Date;
}

export interface UserSignupData {
  username: string;
  email: string;
  password: string;
}

export interface UserLoginData {
  email: string;
  password: string;
}

export interface UserProfileData {
  id: string;
  user_id?: number;
  first_name?: string;
  last_name?: string;
  gender?: string;
  email?: string;
  phone?: string;
  created_at?: Date;
  updated_at?: Date;
} 