import { createContext, useState, useEffect, Dispatch, SetStateAction } from 'react';
import { User } from '../types/auth.types';
import api from '../services/api';

interface AuthContextType {
  user: User | null;
  setUser: Dispatch<SetStateAction<User | null>>;
  isLoading: boolean;
  isAuthenticated: boolean;
}

export const AuthContext = createContext<AuthContextType>({
  user: null,
  setUser: () => {},
  isLoading: true,
  isAuthenticated: false,
});

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          const { data } = await api.get('/users/me');
          setUser(data);
        } catch (error) {
          localStorage.removeItem('token');
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, isLoading, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};
