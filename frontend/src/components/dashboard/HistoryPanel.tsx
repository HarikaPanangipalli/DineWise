import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMealPlan } from '../../hooks/useMealPlan';
import { MealPlanTemp } from '../../types/mealplan.types';

interface HistoryPanelProps {
  onPlanSelect: (plan: MealPlanTemp) => void;
}

export const HistoryPanel: React.FC<HistoryPanelProps> = ({ onPlanSelect }) => {
  const navigate = useNavigate();
  const { getMealPlanHistory, isLoading } = useMealPlan();
  const [history, setHistory] = useState<MealPlanTemp[]>([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getMealPlanHistory();
        setHistory(data.meal_plans);
      } catch (error) {
        console.error('Failed to fetch meal plan history:', error);
      }
    };

    fetchHistory();
  }, [getMealPlanHistory]);

  return (
    <div className="h-full flex flex-col">
      {/* Logo Section - Fixed height */}
      <div className="bg-white h-16 min-h-[64px] flex items-center px-6 border-b border-gray-200">
        <h2 
          onClick={() => window.location.reload()} // Refresh the page
          className="text-2xl font-bold text-indigo-600 cursor-pointer hover:text-indigo-700 transition-colors"
        >
          DineWise
        </h2>
      </div>

      
      {/* Rest of the component remains the same */}
      <div className="h-14 min-h-[56px] flex items-center px-6">
        <h3 className="text-lg font-semibold text-gray-700">History</h3>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-3">
          {history.map((plan) => (
            <div 
              key={plan.meal_plan_id} 
              className="p-4 bg-white rounded-lg shadow-sm hover:bg-indigo-50 transition-colors"
              onClick={() => onPlanSelect(plan)}
            >
              <div className="flex items-center space-x-2">
                <span className="text-indigo-600">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </span>
                <div className="font-medium">{new Date(plan.created_at).toLocaleDateString()}</div>
              </div>
              <div className="mt-1 text-sm text-gray-500">{plan.strategy_used}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};