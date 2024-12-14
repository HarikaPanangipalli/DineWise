import { GenerateMealPlanRequest } from '../types/mealplan.types';
export declare const mealPlanService: {
    generateMealPlan(request: GenerateMealPlanRequest): Promise<any>;
    getMealPlanHistory(): Promise<any>;
    getMealPlanById(id: string): Promise<any>;
};
