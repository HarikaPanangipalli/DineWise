import { User, UserPreferences } from '../types/auth.types';
export declare const useAuth: () => {
    user: User | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    register: (userData: {
        email: string;
        password: string;
        full_name: string;
        preferences: UserPreferences;
    }) => Promise<{
        success: boolean;
        message: string;
    }>;
    logout: () => void;
};
