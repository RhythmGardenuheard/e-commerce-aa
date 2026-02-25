export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Product {
  id: number;
  name: string;
  description?: string;
  price: number;
  stock: number;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}