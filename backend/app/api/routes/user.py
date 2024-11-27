from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserUpdate, User
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user

router = APIRouter()
auth_service = AuthService()

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=User)
async def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    # Convert the `UserUpdate` object to a dictionary
    updated_data = user_update.dict(exclude_unset=True)  # Exclude fields not explicitly set
    
    # Update the user in the database
    updated_user = await auth_service.update_user(current_user.id, updated_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Convert UserInDB to User for the response
    return User(**updated_user.dict())

