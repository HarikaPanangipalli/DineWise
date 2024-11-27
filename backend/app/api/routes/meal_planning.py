"""
This module contains the meal_planning logic.

Classes and methods:
- Provide authentication, service, or model functionality.
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from app.schemas.meal_plan import MealPlanCreate, MealPlanResponse
from app.services.meal_planning_service import MealPlanningService
from app.schemas.user import UserResponse
from app.schemas.meal_plan import MealPlanRequest
from app.api.dependencies import get_current_user
from app.strategies.recommendation_strategy import GeminiAIStrategy
from typing import Optional

router = APIRouter()
meal_plan_service = MealPlanningService()


@router.get("/available-strategies")
async def get_available_strategies(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get list of available meal plan generation strategies"""
    return {
        "strategies": [
            {
                "name": "gemini",
                "description": "Uses Google's Gemini AI for meal plan generation"
            },
            {
                "name": "chatgpt",
                "description": "Uses OpenAI's ChatGPT for meal plan generation"
            }
        ]
    }


@router.post("/generate-meal-plan")
async def generate_meal_plan(
    request: MealPlanRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """Generate meal plan using user's latest groceries and preferences"""
    try:
        # Set strategy based on input
        # print("STRATEGY", strategy)
        # print("additional_preferences", additional_preferences)
        print("request", request)
        if request.strategy.lower() == "chatgpt":
            meal_plan_service.set_strategy(ChatGPTStrategy())
        else:
            meal_plan_service.set_strategy(GeminiAIStrategy())
        
        # Generate meal plan
        result = await meal_plan_service.generate_meal_plan(
            user_id=current_user.id,
            additional_preferences=request.additional_preferences
        )
        
        return {
            "message": "Meal plan generated successfully",
            "meal_plan_id": result["id"],
            "grocery_list_id": result["grocery_list_id"],
            "strategy_used": result["strategy_used"],
            "meal_plan": {
                "meal_plan": result["meal_plan"]["meal_plan"],
                "preferences": result["meal_plan"]["preferences"],
                "grocery_list": result["meal_plan"]["grocery_list"]
            },
            "created_at": result["created_at"]
        }
    

        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    

@router.get("/history")
async def get_meal_plan_history(current_user: UserResponse = Depends(get_current_user)):
    """Get user's meal plan history"""
    try:
        result = await meal_plan_service.get_meal_plan_history(current_user.id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )