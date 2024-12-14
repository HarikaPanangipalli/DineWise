import { LoginCredentials, RegisterData, User } from '../types/auth.types';
export declare const authService: {
    login(credentials: LoginCredentials): Promise<any>;
    register(userData: RegisterData): Promise<any>;
    getCurrentUser(): Promise<User>;
    updatePassword(currentPassword: string, newPassword: string): Promise<any>;
    verifyToken(): Promise<User | null>;
    logout(): void;
    getToken(): string | null;
    getStoredUser(): User | null;
    setupTokenInterceptor(): void;
};
