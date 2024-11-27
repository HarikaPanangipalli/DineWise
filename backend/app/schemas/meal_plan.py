from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class MealPlanBase(BaseModel):
    """Base meal plan model with common attributes"""
    cuisine: str
    dietary_restrictions: List[str] = []

class MealPlanRequest(BaseModel):
    """Model for incoming meal plan requests"""
    additional_preferences: str
    strategy: str = "gemini"

class MealPlanCreate(MealPlanBase):
    """Model for creating a new meal plan"""
    user_id: str
    date: date
    meals: Optional[str] = None

    class Config:
        from_attributes = True

class MealPlan(MealPlanBase):
    """Model for meal plan data"""
    cuisine: str
    dietary_restrictions: List[str]
    meals: str

class MealPlanResponse(MealPlanBase):
    """Model for meal plan API responses"""
    id: str
    user_id: str
    date: date
    meals: str

    class Config:
        from_attributes = True

class MealPlanUpdate(BaseModel):
    """Model for updating existing meal plans"""
    cuisine: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = None
    meals: Optional[str] = None

    class Config:
        from_attributes = True

class GenerateMealPlanRequest(BaseModel):
    """Model for meal plan generation requests"""
    preferences: str
    grocery_list: str
    strategy: Optional[str] = "gemini"  # Default to Gemini strategy

class GenerateMealPlanResponse(BaseModel):
    """Model for meal plan generation responses"""
    strategy_used: str
    meal_plan: dict
    preferences: str
    grocery_list: str