export interface MealPlan {
    id: string;
    user_id: string;
    grocery_list_id: string;
    meals: {
        breakfast: string[];
        lunch: string[];
        dinner: string[];
    };
    created_at: string;
    strategy_used: string;
}
export interface GenerateMealPlanRequest {
    additional_preferences?: string;
    strategy: string;
}
interface MealPlanData {
    [key: string]: string;
}
export interface MealPlanTemp {
    message: string;
    meal_plan_id: string;
    grocery_list_id: string;
    strategy_used: string;
    created_at: string;
    meal_plan: MealPlanData;
    preferences: string;
    grocery_list: string;
}
export {};
