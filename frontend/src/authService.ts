// src/services/authService.ts
import { useAuth } from '../contexts/AuthContext';

// Types
export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// For login using OAuth2 password flow
export const loginUser = async (data: LoginData): Promise<TokenResponse> => {
  const formData = new FormData();
  formData.append('username', data.email); // FastAPI OAuth2 expects 'username' field
  formData.append('password', data.password);

  const response = await fetch('/auth/login', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Login failed');
  }

  return response.json();
};

// For user registration
export const registerUser = async (data: RegisterData): Promise<TokenResponse> => {
  const response = await fetch('/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Registration failed');
  }

  return response.json();
};