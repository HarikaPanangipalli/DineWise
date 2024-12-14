//useAuth.tsx
import { useContext, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import api from '../services/api';
import { User, UserPreferences } from '../types/auth.types';

interface AuthResponse {
  access_token: string;
  user: User;
}

export const useAuth = () => {
  const navigate = useNavigate();
  const { user, setUser, isLoading } = useContext(AuthContext);

  const login = useCallback(async (email: string, password: string) => {
    try {
      const { data: authData } = await api.post<AuthResponse>(
        '/auth/token', 
        new URLSearchParams({
          username: email,
          password: password
        }), 
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );

      localStorage.setItem('token', authData.access_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${authData.access_token}`;
      const { data: userData } = await api.get<User>('/users/me');
      localStorage.setItem('user', JSON.stringify(userData)); // Store user data
      setUser(userData);

      navigate('/gmail-auth');
    } catch (error) {
      localStorage.removeItem('token');
      localStorage.removeItem('user'); // Clean up user data
      throw new Error('Invalid credentials');
    }
  }, [navigate, setUser]);

  const register = useCallback(async (userData: {
      email: string;
      password: string;
      full_name: string;
      preferences: UserPreferences;
  }) => {
      try {
          const { data } = await api.post<User>('/auth/register', userData);
          
          return { success: true, message: 'Registration successful!' };
      } catch (error: any) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          
          if (error.response?.status === 400) {
              throw new Error('Email already registered');
          }
          throw new Error('Registration failed. Please try again.');
      }
  }, [setUser]);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
    navigate('/login');
  }, [navigate, setUser]);

  return { user, isLoading, isAuthenticated: !!user, login, register, logout };
};
