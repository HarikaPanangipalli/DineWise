from pydantic import BaseModel
from datetime import datetime
from typing import List


class MealPlanInDB(BaseModel):
    """
    Represents a meal plan stored in the database.

    Attributes:
        id (str): Unique identifier for the meal plan.
        user_id (str): Identifier for the user who created the meal plan.
        cuisine (str): The cuisine type for the meal plan.
        dietary_restrictions (List[str]): Dietary restrictions considered in the plan.
        meals (str): JSON string containing structured meal data.
        created_at (datetime): Timestamp when the meal plan was created.
    """

    id: str
    user_id: str
    cuisine: str
    dietary_restrictions: List[str]
    meals: str  # This could be a JSON string representing structured meal data
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
