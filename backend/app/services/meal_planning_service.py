# app/services/meal_planning_service.py
"""
Meal Planning Service

Provides functionality to generate meal plans based on user preferences and grocery items.

Classes:
- MealPlanningService: Core service for meal planning.

Methods:
- generate_meal_plan: Creates a meal plan using AI.
"""
from app.db.database import database
from datetime import datetime
import uuid
from bson import ObjectId
import re


class MealPlanningService:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy):
        self._strategy = strategy

    async def get_latest_grocery_list_id(self, user_id: str) -> str:
        """Get user's latest grocery list ID"""
        try:
            latest_grocery = await database.db.groceries.find_one(
                {"user_id": user_id}, sort=[("created_at", -1)]
            )
            if not latest_grocery:
                raise Exception("No grocery list found for user")
            return str(latest_grocery["_id"])  # Convert ObjectId to string
        except Exception as e:
            raise Exception(f"Failed to fetch latest grocery list: {str(e)}")

    async def get_user_preferences(self, user_id: str) -> dict:
        """Get user's preferences"""
        try:
            user = await database.db.users.find_one({"id": user_id})
            return user.get("preferences", {}) if user else {}
        except Exception as e:
            raise Exception(f"Failed to fetch user preferences: {str(e)}")

    async def generate_meal_plan(
        self, user_id: str, additional_preferences: str = ""
    ) -> dict:
        """Generate meal plan using user's groceries and preferences"""
        try:
            # Get latest grocery list ID

            grocery_list_id = await self.get_latest_grocery_list_id(user_id)

            # Delete previous meal plan for this grocery list
            await database.db.meal_plans.delete_many(
                {"user_id": user_id, "grocery_list_id": grocery_list_id}
            )

            # Get the actual grocery items for meal planning
            grocery_list = await database.db.groceries.find_one(
                {"_id": ObjectId(grocery_list_id)}
            )

            if not grocery_list or not grocery_list.get("items"):
                raise Exception("No grocery items found")

            # Get user preferences
            user_prefs = await self.get_user_preferences(user_id)

            grocery_items = [
                item["item_name"] for item in grocery_list.get("items", [])
            ]

            # Combine preferences
            combined_preferences = f"""
            Cuisine preferences: {', '.join(user_prefs.get('cuisine_preferences', []))}
            Dietary restrictions: {', '.join(user_prefs.get('dietary_restrictions', []))}
            Allergies: {', '.join(user_prefs.get('allergies', []))}
            Additional preferences: {additional_preferences}
            """
            print(self._strategy.__class__)
            if not self._strategy:
                raise Exception("No meal planning strategy selected")

            # Generate meal plan
            meal_plan = await self._strategy.generate_meal_plan(
                preferences=combined_preferences, grocery_list=grocery_items
            )

            formatted_meal_plan = self.format_meal_plan(meal_plan.get("meal_plan"))

            meal_plan_data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "grocery_list_id": grocery_list_id,  # Store reference instead of full list
                "preferences_used": combined_preferences,
                "meal_plan": {
                    "meal_plan": formatted_meal_plan,
                    "preferences": combined_preferences,
                    "grocery_list": meal_plan.get("grocery_list"),
                },
                "created_at": datetime.utcnow(),
                "strategy_used": self._strategy.__class__.__name__,
            }

            result = await database.db.meal_plans.insert_one(meal_plan_data)
            if not result.inserted_id:
                raise Exception("Failed to store meal plan")

            # Return response without ObjectId
            return {
                "id": meal_plan_data["id"],
                "user_id": user_id,
                "grocery_list_id": grocery_list_id,
                "meal_plan": {
                    "meal_plan": formatted_meal_plan,
                    "preferences": combined_preferences,
                    "grocery_list": meal_plan.get("grocery_list"),
                },
                "strategy_used": meal_plan_data["strategy_used"],
                "created_at": meal_plan_data["created_at"].isoformat(),
            }

        except Exception as e:
            raise Exception(f"Failed to generate meal plan: {str(e)}")

    async def get_meal_plan_history(self, user_id: str) -> list:
        """Get user's meal plan history"""
        try:
            # Find all meal plans for the user, sorted by creation date
            cursor = database.db.meal_plans.find(
                {"user_id": user_id}, sort=[("created_at", -1)]
            )

            meal_plans = []
            async for plan in cursor:
                # Format the meal plan data
                meal_plan = {
                    "id": str(plan["_id"]),  # Convert ObjectId to string
                    "created_at": plan["created_at"],
                    "strategy_used": plan["strategy_used"],
                    "grocery_list_id": str(
                        plan["grocery_list_id"]
                    ),  # Convert ObjectId to string
                    "meal_plan": plan["meal_plan"],
                }
                meal_plans.append(meal_plan)

            return {"total": len(meal_plans), "meal_plans": meal_plans}

        except Exception as e:
            print(f"Error fetching meal plan history: {str(e)}")
            raise Exception(f"Failed to fetch meal plan history: {str(e)}")

    def format_meal_plan(self, meal_plan: str) -> dict:
        # Initialize the dictionary
        meal_dict = {}

        # Split the string by days using a regular expression
        days = re.split(r"\*\*Day \d+\*\*", meal_plan)[1:]

        # Iterate over each day's data
        for i, day_data in enumerate(days, 1):
            day_key = f"Day_{i}"
            meals = {}

            # Extract meals (Breakfast, Lunch, Dinner)
            for meal in ["Breakfast", "Lunch", "Dinner"]:
                meal_match = re.search(
                    rf"\* \*\*{meal}:\*\* (.+?)(?=\n\*|$)", day_data, re.DOTALL
                )
                if meal_match:
                    meals[meal] = meal_match.group(1).strip()

            # Assign to the day's key in the dictionary
            meal_dict[day_key] = meals

        return meal_dict
