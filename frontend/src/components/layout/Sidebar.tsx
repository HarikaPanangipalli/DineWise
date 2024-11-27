import { useNavigate } from 'react-router-dom';
import { useMealPlan } from '../../hooks/useMealPlan';

export const Sidebar = () => {
  const navigate = useNavigate();
  const { getMealPlanHistory, isLoading } = useMealPlan();

  return (
    <div className="h-full bg-gray-800 text-white w-64 flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-xl font-semibold">Meal Plan History</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {isLoading ? (
          <div className="flex justify-center items-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
          </div>
        ) : (
          <div className="space-y-4">
            {/* History items will be mapped here */}
          </div>
        )}
      </div>

      <div className="p-4 border-t border-gray-700">
        <button
          onClick={() => navigate('/generate')}
          className="w-full py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          Generate New Plan
        </button>
      </div>
    </div>
  );
};