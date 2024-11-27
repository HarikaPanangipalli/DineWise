// src/components/dashboard/MealPlanGenerator.tsx
import { useState } from 'react';
import { useMealPlan } from '../../hooks/useMealPlan';
import { MealPlanDisplay } from './MealPlanDisplay';
import { MealPlan } from '../../types/mealplan.types';

export const MealPlanGenerator = () => {
  const { generateMealPlan, isLoading } = useMealPlan();
  const [mealPlan, setMealPlan] = useState<MealPlan | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedStrategy, setSelectedStrategy] = useState('gemini');

  const handleGenerateMealPlan = async () => {
    try {
      setError(null);
      const generatedPlan = await generateMealPlan({
        additional_preferences: '',
        strategy: selectedStrategy
      });
      setMealPlan(generatedPlan);
    } catch (err) {
      setError('Failed to generate meal plan. Please try again.');
      console.error('Meal plan generation failed:', err);
    }
  };

  if (!mealPlan) {
    return (
      <div className="flex flex-col items-center justify-center">
        {error && (
          <div className="mb-4 p-4 bg-red-50 text-red-600 rounded-lg w-full max-w-md">
            {error}
          </div>
        )}
        
        <div className="flex items-center gap-4 w-full max-w-md">
          <button
            onClick={handleGenerateMealPlan}
            disabled={isLoading}
            className="px-6 py-4 bg-[#6366F1] text-white text-lg font-medium rounded-xl hover:bg-[#5558E3] disabled:opacity-50 flex items-center justify-center"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating...
              </>
            ) : (
              'Generate Meal Plan'
            )}
          </button>
          <select
            value={selectedStrategy}
            onChange={(e) => setSelectedStrategy(e.target.value)}
            className="px-4 py-4 border border-gray-300 rounded-xl text-gray-700 flex-1 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="gemini">Gemini AI</option>
            {/* <option value="chatgpt">ChatGPT AI</option> */}
          </select>
        </div>
        <div className="mt-4 px-4 text-sm text-gray-500">
             Click the button to generate a personalized meal plan based on your groceries and preferences.
        </div>
      </div>
    );
  }

  return (
    <div>
      <MealPlanDisplay plan={mealPlan} history={false}/>
      <button
        onClick={() => setMealPlan(null)}
        className="mt-6 w-full py-2 text-indigo-600 hover:text-indigo-700 border border-indigo-600 rounded-lg"
      >
        Generate Another Plan
      </button>
    </div>
  );
};