// src/components/dashboard/MealPlanDisplay.tsx
import { MealPlanTemp } from '../../types/mealplan.types';

interface MealPlanDisplayProps {
  plan: MealPlanTemp;
  history: Boolean
}

export const MealPlanDisplay: React.FC<MealPlanDisplayProps> = ({ plan, history=true }) => {
  const formatMealPlan = (mealPlanData: any) => {
    if (!mealPlanData || !mealPlanData.meal_plan) {
      return [];
    }

    try {
      return Object.entries(mealPlanData.meal_plan).map(([day, meals]) => {
        return {
          day: day.replace('_', ' '),
          meals: meals as Record<string, string>
        };
      });
    } catch (error) {
      console.error('Error formatting meal plan:', error);
      return [];
    }
  };

  return (
    <div className="space-y-6">      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {formatMealPlan(plan.meal_plan).map((day, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="bg-indigo-600 px-4 py-3">
              <h3 className="text-lg font-semibold text-white">{day.day}</h3>
            </div>
            <div className="p-4 space-y-4">
              <div>
                <h4 className="text-sm font-bold text-indigo-600 uppercase mb-2">Breakfast</h4>
                <p className="text-sm text-gray-600">{day.meals.Breakfast}</p>
              </div>
              <div>
                <h4 className="text-sm font-bold text-indigo-600 uppercase mb-2">Lunch</h4>
                <p className="text-sm text-gray-600">{day.meals.Lunch}</p>
              </div>
              <div>
                <h4 className="text-sm font-bold text-indigo-600 uppercase mb-2">Dinner</h4>
                <p className="text-sm text-gray-600">{day.meals.Dinner}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {plan.meal_plan.preferences && history &&(
        <div className="mt-8 p-4 bg-white rounded-lg shadow">
          <h3 className="text-lg font-semibold text-indigo-600 mb-2">Preferences</h3>
          <pre className="whitespace-pre-wrap text-sm text-gray-600">
          {plan.meal_plan.preferences
            .split("\n")
            .map(item => item.trim()) // Remove spaces from each item
            .filter(item => item !== "") // Remove empty strings
            .map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </pre>
        </div>
      )}

      {plan.meal_plan.grocery_list && history && (
        <div className="mt-4 p-4 bg-white rounded-lg shadow">
          <h3 className="text-lg font-semibold text-indigo-600 mb-2">Grocery List</h3>
          <ul className="list-disc pl-5 space-y-1 text-sm text-gray-600">
            {plan.meal_plan.grocery_list.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};