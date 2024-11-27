from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List

class UserPreferencesInDB(BaseModel):
    """
    Represents user preferences and dietary restrictions.

    Attributes:
        cuisine_preferences (List[str]): List of preferred cuisines.
        dietary_restrictions (List[str]): List of dietary restrictions (e.g., vegan, gluten-free).
        allergies (List[str]): List of food allergies.
        cooking_skill_level (str): User's cooking skill level (e.g., beginner, intermediate, expert).
    """
    cuisine_preferences: List[str] = []
    dietary_restrictions: List[str] = []
    allergies: List[str] = []
    cooking_skill_level: str = "intermediate"

    model_config = ConfigDict(from_attributes=True)

class UserInDB(BaseModel):
    id: str
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    preferences: Optional[UserPreferencesInDB] = None
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()

    def update_preferences(self, preferences: UserPreferencesInDB):
        self.preferences = preferences
        self.update_timestamp()