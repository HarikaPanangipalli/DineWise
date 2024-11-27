import api from './api';
import { GenerateMealPlanRequest, MealPlan } from '../types/mealplan.types';

export const mealPlanService = {
  async generateMealPlan(request: GenerateMealPlanRequest) {
    const { data } = await api.post('/meal-planning/generate-meal-plan', {
      additional_preferences: request.additional_preferences,
      strategy: request.strategy
    });
    return data;
  },

  async getMealPlanHistory() {
    const { data } = await api.get('/meal-planning/history');
    return data;
  },

  async getMealPlanById(id: string) {
    const { data } = await api.get(`/meal-planning/${id}`);
    return data;
  },
};