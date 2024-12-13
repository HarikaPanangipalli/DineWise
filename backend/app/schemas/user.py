from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserPreferences(BaseModel):
    cuisine_preferences: List[str] = []
    dietary_restrictions: List[str] = []
    allergies: List[str] = []
    cooking_skill_level: str = "intermediate"

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    preferences: Optional[UserPreferences] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class ForgotPasswordReset(BaseModel):
    email: EmailStr
    reset_token: str
    new_password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str
    is_active: bool = True
    preferences: Optional[UserPreferences] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    id: str
    is_active: bool = True
    preferences: Optional[UserPreferences] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
