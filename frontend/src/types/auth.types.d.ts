export interface UserPreferences {
    cuisine_preferences: string[];
    dietary_restrictions: string[];
    allergies: string[];
    cooking_skill_level: string;
}
export interface User {
    id?: string;
    email: string;
    full_name: string;
    preferences: UserPreferences;
    is_active: boolean;
}
export interface LoginCredentials {
    username: string;
    password: string;
}
export interface RegisterData extends LoginCredentials {
    full_name: string;
    preferences: UserPreferences;
}
