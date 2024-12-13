from abc import ABC, abstractmethod
import google.generativeai as genai

# from openai import OpenAI
# import openai
from app.core.config import settings
from typing import Optional, Dict, Any


class RecommendationStrategy(ABC):
    @abstractmethod
    async def generate_meal_plan(self, preferences: str, grocery_list: str) -> dict:
        pass


class GeminiAIStrategy(RecommendationStrategy):
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    async def generate_meal_plan(self, preferences: str, grocery_list: str) -> dict:
        try:
            prompt = self._create_prompt(preferences, grocery_list)
            response = await self.model.generate_content_async(prompt)
            return {
                "model": "gemini",
                "meal_plan": response.text,
                "preferences": preferences,
                "grocery_list": grocery_list,
            }
        except Exception as e:
            raise Exception(f"Gemini meal plan generation failed: {str(e)}")

    def _create_prompt(self, combined_preferences: str, grocery_list: str) -> str:
        return f"""
                Create a comprehensive meal plan using these groceries: {grocery_list}

                Consider these preferences and restrictions:
                {combined_preferences}

                Important guidelines:
                1. Suggest new dishes for each meal, considering all preferences
                2. Do not recommend leftover foods
                3. Continue planning meals until ALL groceries are completely used up
                4. The number of days in the meal plan should be determined by how long it takes to use all groceries
                5. If main ingredients are used up before all groceries, suggest creative ways to use remaining items

                Formatting rules:
                1. Format each meal as follows:
                **Day X**

                * **Breakfast:** [Meal] (made with [ingredients])
                * **Lunch:** [Meal] (made with [ingredients])
                * **Dinner:** [Meal] (made with [ingredients])

                2. Continue adding days until all groceries are utilized, even if it exceeds 7 days
                3. Specify ingredients from the grocery list in parentheses for each meal
                4. Use double asterisks for bold text
                5. Include two newlines between days and one newline between meals within a day
                6. At the end of the meal plan, confirm that all groceries have been used

                Begin the meal plan with Day 1 and continue until all groceries are used. The meal plan should end only when all groceries have been incorporated into meals.
            """

    # class ChatGPTStrategy(RecommendationStrategy):
    #     def __init__(self):
    #         self.model = "gpt-4"
    #         OpenAI.OpenAI = settings.openai_api_key
    #         client = OpenAI()

    #     async def generate_meal_plan(self, preferences: str, grocery_list: str) -> dict:
    #         try:
    #             prompt = self._create_prompt(preferences, grocery_list)

    #             client = OpenAI()
    #             client.api_key = settings.openai_api_key

    #             completion = client.chat.completions.create(
    #                 model="gpt3",
    #                 messages=[
    #                     {"role": "user", "content": prompt}
    #                 ],
    #                 max_tokens=1000
    #             )

    #             return {
    #                 "model": "chatgpt",
    #                 "meal_plan": completion.choices[0].message,
    #                 "preferences": preferences,
    #                 "grocery_list": grocery_list
    #             }
    #         except Exception as e:
    #             raise Exception(f"ChatGPT meal plan generation failed: {str(e)}")

    def _create_prompt(self, combined_preferences: str, grocery_list: str) -> str:
        return f"""
                Create a comprehensive meal plan using these groceries: {grocery_list}

                Consider these preferences and restrictions:
                {combined_preferences}

                Important guidelines:
                1. Suggest new dishes for each meal, considering all preferences
                2. Do not recommend leftover foods
                3. Continue planning meals until ALL groceries are completely used up
                4. The number of days in the meal plan should be determined by how long it takes to use all groceries
                5. If main ingredients are used up before all groceries, suggest creative ways to use remaining items

                Formatting rules:
                1. Format each meal as follows:
                **Day X**

                * **Breakfast:** [Meal] (made with [ingredients])
                * **Lunch:** [Meal] (made with [ingredients])
                * **Dinner:** [Meal] (made with [ingredients])

                2. Continue adding days until all groceries are utilized, even if it exceeds 7 days
                3. Specify ingredients from the grocery list in parentheses for each meal
                4. Use double asterisks for bold text
                5. Include two newlines between days and one newline between meals within a day
                6. At the end of the meal plan, confirm that all groceries have been used

                Begin the meal plan with Day 1 and continue until all groceries are used. The meal plan should end only when all groceries have been incorporated into meals.
            """


class MealPlanningService:
    def __init__(self):
        self._strategy: Optional[RecommendationStrategy] = None
        self.set_strategy(GeminiAIStrategy())  # Default strategy

    def set_strategy(self, strategy: RecommendationStrategy):
        """Set the meal plan generation strategy"""
        self._strategy = strategy

    async def generate_meal_plan(self, preferences: str, grocery_list: str) -> dict:
        """Generate meal plan using current strategy"""
        if not self._strategy:
            raise Exception("No meal planning strategy selected")
        try:
            return await self._strategy.generate_meal_plan(preferences, grocery_list)
        except Exception as e:
            raise Exception(f"Failed to generate meal plan: {str(e)}")
