"""
This module contains the auth logic.

Classes and methods:
- Provide authentication, service, or model functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import (
    UserCreate,
    User,
    PasswordReset,
    ForgotPasswordReset,
    PasswordUpdate,
)
from app.services.auth_service import AuthService
from app.core.security import create_access_token
from app.api.dependencies import get_current_user

router = APIRouter()
auth_service = AuthService()


@router.post("/register")
async def register_user(user: UserCreate):
    try:
        # Create user with preferences
        created_user = await auth_service.create_user(user)
        return created_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to register user: {str(e)}"
        )


# @router.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await auth_service.authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password")
async def forgot_password(password_reset: PasswordReset):
    """
    Request a password reset token
    """
    return await auth_service.create_password_reset_token(password_reset.email)


@router.post("/reset-password")
async def reset_password(reset_data: ForgotPasswordReset):
    """
    Reset password using the reset token
    """
    return await auth_service.reset_password(reset_data)


@router.post("/update-password")
async def update_password(
    password_update: PasswordUpdate, current_user: User = Depends(get_current_user)
):
    """
    Update password for logged-in user
    """
    return await auth_service.update_password(current_user.id, password_update)


@router.get("/callback")
async def auth_callback(code: str = None, error: str = None):
    """Handle Gmail OAuth callback"""
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Authentication successful"}


@router.get("/gmail/callback")
async def gmail_auth_callback(code: str = None, error: str = None):
    """Handle Gmail OAuth callback"""
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Gmail authentication successful"}


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})

    # Return user data along with token
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "preferences": user.preferences,
        },
    }


@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    """Verify token and return user data"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "preferences": current_user.preferences,
    }
