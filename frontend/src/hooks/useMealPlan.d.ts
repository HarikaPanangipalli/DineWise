import { GenerateMealPlanRequest } from '../types/mealplan.types';
export declare const useMealPlan: () => {
    isLoading: boolean;
    error: string | null;
    generateMealPlan: (request: GenerateMealPlanRequest) => Promise<any>;
    getMealPlanHistory: () => Promise<any>;
};
