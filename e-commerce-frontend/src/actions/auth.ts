'use server';

import { LoginData, Token } from '@/types';

const API_BASE_URL = 'http://localhost:8000'; // Adjust to your backend URL

export async function loginUser(data: LoginData): Promise<Token> {
  const formData = new FormData();
  formData.append('username', data.username);
  formData.append('password', data.password);

  const response = await fetch(`${API_BASE_URL}/token`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  return response.json();
}

export async function registerUser(data: { username: string; email: string; password: string }) {
  const response = await fetch(`${API_BASE_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Registration failed');
  }

  return response.json();
}