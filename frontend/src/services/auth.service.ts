// import api from './api';
// import { LoginCredentials, RegisterData, User } from '../types/auth.types';

// export const authService = {
//   async login(credentials: LoginCredentials) {
//     const { data } = await api.post('/auth/token', credentials);
//     return data;
//   },

//   async register(userData: RegisterData) {
//     const { data } = await api.post('/auth/register', userData);
//     return data;
//   },

//   async getCurrentUser(): Promise<User> {
//     const { data } = await api.get('/auth/me');
//     return data;
//   },

//   async updatePassword(currentPassword: string, newPassword: string) {
//     const { data } = await api.put('/auth/update-password', {
//       current_password: currentPassword,
//       new_password: newPassword,
//     });
//     return data;
//   },
// };


import api from './api';
import { LoginCredentials, RegisterData, User } from '../types/auth.types';

const TOKEN_KEY = 'auth_token';
const USER_KEY = 'user_data';

export const authService = {
  async login(credentials: LoginCredentials) {
    const { data } = await api.post('/auth/token', credentials);
    if (data.access_token) {
      localStorage.setItem(TOKEN_KEY, data.access_token);
      localStorage.setItem(USER_KEY, JSON.stringify(data.user));
      api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;
    }
    return data;
  },

  async register(userData: RegisterData) {
    const { data } = await api.post('/auth/register', userData);
    return data;
  },

  async getCurrentUser(): Promise<User> {
    const { data } = await api.get('/auth/me');
    return data;
  },

  async updatePassword(currentPassword: string, newPassword: string) {
    const { data } = await api.put('/auth/update-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
    return data;
  },

  async verifyToken(): Promise<User | null> {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) return null;

    try {
      const { data } = await api.get('/auth/verify-token');
      return data;
    } catch (error) {
      this.logout();
      return null;
    }
  },

  logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    delete api.defaults.headers.common['Authorization'];
  },

  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  getStoredUser(): User | null {
    const userData = localStorage.getItem(USER_KEY);
    return userData ? JSON.parse(userData) : null;
  },

  setupTokenInterceptor() {
    const token = this.getToken();
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }
};