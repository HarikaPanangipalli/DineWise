import { useState, useCallback } from 'react';
import { mealPlanService } from '../services/mealplan.service';
import { MealPlan, GenerateMealPlanRequest } from '../types/mealplan.types';

export const useMealPlan = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateMealPlan = useCallback(async (request: GenerateMealPlanRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const mealPlan = await mealPlanService.generateMealPlan(request);
      console.log("Generated Meal Plan", mealPlan)
      return mealPlan;
    } catch (err) {
      setError('Failed to generate meal plan');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const getMealPlanHistory = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const history = await mealPlanService.getMealPlanHistory();
      return history;
    } catch (err) {
      setError('Failed to fetch meal plan history');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    isLoading,
    error,
    generateMealPlan,
    getMealPlanHistory,
  };
};