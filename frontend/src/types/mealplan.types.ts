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

  // export interface MealPlanTemp {
  //   id: string;
  //   user_id: string; // Assuming a user_id field, you can replace or remove if not applicable
  //   grocery_list_id: string;
  //   meals: {
  //     breakfast: string[];
  //     lunch: string[];
  //     dinner: string[];
  //   };
  //   created_at: string;
  //   strategy_used: string;
  //   grocery_list: string; // Includes the grocery list as a string
  //   preferences: string; // Includes user preferences as a string
  // }


  // export interface MealPlanTemp {
  //   id: string;
  //   created_at: string;
  //   strategy_used: string;
  //   grocery_list_id: string;
  //   meal_plan: {
  //     model: string;
  //     meal_plan: string;
      
  //     grocery_list: string;
  //   };
  //   preferences: string;
  // }


  interface MealPlanData {
    [key: string]: string;  // Dynamic day keys like "Day_1", "Day_2", etc.
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
  
  