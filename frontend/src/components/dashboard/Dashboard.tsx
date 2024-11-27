// src/components/dashboard/Dashboard.tsx
import { useState } from 'react';
import { HistoryPanel } from './HistoryPanel';
import { MealPlanGenerator } from './MealPlanGenerator';
import { MealPlanDisplay } from './MealPlanDisplay';
import { Header } from '../layout/Header';
import { useAuth } from '../../hooks/useAuth';
import { GroceryList } from './GroceryList';
import api from '../../services/api';

export const Dashboard = () => {
  const { user } = useAuth();
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [groceries, setGroceries] = useState(null);
  const [isExtracting, setIsExtracting] = useState(false);
  const [groceryId, setGroceryId] = useState(null);
  const [noGroceriesFound, setNoGroceriesFound] = useState(false);

  const handleExtractGroceries = async () => {
    setIsExtracting(true);
    setNoGroceriesFound(false);
    try {
      const responseExtractGroceries = await api.get('/gmail/extract-groceries');
      if (responseExtractGroceries.status == 200 && responseExtractGroceries.data.total_items > 0) {
        const responseGroceryList = await api.get('/grocery/' + responseExtractGroceries.data.grocery_list_id);
        setGroceries(responseGroceryList.data.items);
        setGroceryId(responseExtractGroceries.data.grocery_list_id);
      } else {
        setNoGroceriesFound(true);
      }
    } catch (error) {
      console.error('Failed to extract groceries:', error);
      console.log('Failed to extract groceries:', error)
      setNoGroceriesFound(true);
    } finally {
      setIsExtracting(false);
    }
  };

  const renderMainContent = () => {
    if (selectedPlan) {
      return (
        <div className="bg-white rounded-lg shadow p-6">
          <button 
            onClick={() => setSelectedPlan(null)}
            className="mb-4 text-indigo-600 hover:text-indigo-700 flex items-center"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Dashboard
          </button>
          <MealPlanDisplay plan={selectedPlan} history={true}/>

        </div>
      );
    }

    return (
      <>
        {/* User Preferences Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Preferences</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-indigo-600 mb-3">
                Cuisine
              </h3>
              <div className="flex flex-wrap gap-2">
                {(user?.preferences?.cuisine_preferences ?? []).length > 0 ? (
                  user?.preferences?.cuisine_preferences?.map((cuisine, index) => (
                    <span key={index} className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm">
                      {cuisine}
                    </span>
                  ))
                ) : (
                  <span className="text-gray-500 text-sm">None</span>
                )}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-indigo-600 mb-3">
                Dietary Restrictions
              </h3>
              <div className="flex flex-wrap gap-2">
                {(user?.preferences?.dietary_restrictions ?? []).length > 0 ? (
                  user?.preferences?.dietary_restrictions?.map((restriction, index) => (
                    <span key={index} className="px-3 py-1 bg-yellow-50 text-yellow-700 rounded-full text-sm">
                      {restriction}
                    </span>
                  ))
                ) : (
                  <span className="text-gray-500 text-sm">None</span>
                )}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-indigo-600 mb-3">
                Allergies
              </h3>
              <div className="flex flex-wrap gap-2">
                {(user?.preferences?.allergies ?? []).length > 0 ? (
                  user?.preferences?.allergies?.map((allergy, index) => (
                    <span key={index} className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm">
                      {allergy}
                    </span>
                  ))
                ) : (
                  <span className="text-gray-500 text-sm">None</span>
                )}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-indigo-600 mb-3">
                Cooking Skill Level
              </h3>
              <span className="px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm">
                {user?.preferences?.cooking_skill_level ?? 'Not specified'}
              </span>
            </div>
          </div>
        </div>

        {/* Groceries Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Groceries</h2>
          <div className="bg-white rounded-lg shadow p-6">
            {!groceries ? (
              <div className="flex flex-col items-center justify-center py-12">
                <button
                  onClick={handleExtractGroceries}
                  disabled={isExtracting || noGroceriesFound}
                  className="w-full max-w-md mx-auto px-6 py-4 bg-[#6366F1] text-white text-lg font-medium rounded-xl hover:bg-[#5558E3] disabled:opacity-50 flex items-center justify-center mb-6"
                >
                  {isExtracting ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Extracting...
                    </>
                  ) : (
                    'Extract Groceries'
                  )}
                </button>
                {noGroceriesFound ? (
                  <div className="text-center">
                    <p className="text-red-500 mb-2">No new groceries found in your emails</p>
                    <p className="text-sm text-gray-500">Please check back later when you have new grocery emails</p>
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">Click the button above to extract groceries from your emails</p>
                )}
              </div>
            ) : (
              <GroceryList 
                groceryId={groceryId}
                groceries={groceries} 
                onUpdate={setGroceries}
              />
            )}
          </div>
        </div>

        {/* Meal Plan Section - Only show when groceries exist */}
        {groceries && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Meal Plan</h2>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex flex-col items-center justify-center py-8">
                <MealPlanGenerator groceries={groceries}/>
              </div>
            </div>
          </div>
        )}
      </>
    );
  };

  return (
    <div className="h-screen bg-gray-50 flex">
      {/* Left Panel - History */}
      <aside className="w-64 bg-white border-r border-gray-200">
        <HistoryPanel onPlanSelect={setSelectedPlan} />
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          {renderMainContent()}
        </main>
      </div>
    </div>
  );
};




