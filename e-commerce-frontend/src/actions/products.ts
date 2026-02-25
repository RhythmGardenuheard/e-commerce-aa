'use server';

import { Product } from '@/types';

const API_BASE_URL = 'http://localhost:8000'; // Adjust to your backend URL

export async function getProducts(token: string): Promise<Product[]> {
  const response = await fetch(`${API_BASE_URL}/products`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }

  return response.json();
}

export async function getProduct(id: number, token: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/products/${id}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch product');
  }

  return response.json();
}

export async function createProduct(data: Omit<Product, 'id'>, token: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/products`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to create product');
  }

  return response.json();
}

export async function updateProduct(id: number, data: Omit<Product, 'id'>, token: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/products/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to update product');
  }

  return response.json();
}

export async function deleteProduct(id: number, token: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/products/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to delete product');
  }
}