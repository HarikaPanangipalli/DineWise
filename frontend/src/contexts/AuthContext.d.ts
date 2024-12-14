import { Dispatch, SetStateAction } from 'react';
import { User } from '../types/auth.types';
interface AuthContextType {
    user: User | null;
    setUser: Dispatch<SetStateAction<User | null>>;
    isLoading: boolean;
    isAuthenticated: boolean;
}
export declare const AuthContext: import("react").Context<AuthContextType>;
interface AuthProviderProps {
    children: React.ReactNode;
}
export declare const AuthProvider: React.FC<AuthProviderProps>;
export {};
