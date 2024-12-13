"""
Authentication Service

This module contains the logic for user authentication, including token generation and user validation.

Classes:
- AuthService: Provides methods for managing user authentication and tokens.

Methods:
- authenticate_user: Verifies user credentials.
- create_access_token: Generates a JWT for user sessions.
"""

from datetime import datetime, timedelta
from app.db.database import database
from app.schemas.user import UserCreate, UserInDB, PasswordUpdate, ForgotPasswordReset
from app.core.security import get_password_hash, verify_password
from app.core.config import settings
from fastapi import HTTPException
import uuid
import jwt

<<<<<<< HEAD

=======
>>>>>>> main
class AuthService:
    """
    Service for handling authentication-related logic.
    """
<<<<<<< HEAD

=======
>>>>>>> main
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes

<<<<<<< HEAD
    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
=======
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
>>>>>>> main
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
<<<<<<< HEAD

=======
        
>>>>>>> main
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def get_user_by_email(self, email: str):
        try:
            user = await database.users.find_one({"email": email})
            if user:
                return UserInDB(**user)
            return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def authenticate_user(self, email: str, password: str):
        """
        Authenticate a user by verifying their username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: The authenticated user object, or None if authentication fails.
        """
        user = await self.get_user_by_email(email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
<<<<<<< HEAD

=======
    
>>>>>>> main
    async def update_password(self, user_id: str, password_update: PasswordUpdate):
        try:
            user = await database.users.find_one({"id": user_id})
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
<<<<<<< HEAD

            if not verify_password(
                password_update.current_password, user["hashed_password"]
            ):
                raise HTTPException(status_code=400, detail="Incorrect password")

=======
            
            if not verify_password(password_update.current_password, user["hashed_password"]):
                raise HTTPException(status_code=400, detail="Incorrect password")
            
>>>>>>> main
            hashed_password = get_password_hash(password_update.new_password)
            await database.users.update_one(
                {"id": user_id},
                {
                    "$set": {
                        "hashed_password": hashed_password,
<<<<<<< HEAD
                        "updated_at": datetime.utcnow(),
                    }
                },
=======
                        "updated_at": datetime.utcnow()
                    }
                }
>>>>>>> main
            )
            return {"message": "Password updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_password_reset_token(self, email: str):
        try:
            user = await self.get_user_by_email(email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
<<<<<<< HEAD

            # Create reset token
            reset_token = self.create_access_token(
                data={"sub": email, "type": "password_reset"},
                expires_delta=timedelta(minutes=15),
            )

=======
            
            # Create reset token
            reset_token = self.create_access_token(
                data={"sub": email, "type": "password_reset"},
                expires_delta=timedelta(minutes=15)
            )
            
>>>>>>> main
            # Store reset token in database
            await database.users.update_one(
                {"email": email},
                {
                    "$set": {
                        "reset_token": reset_token,
<<<<<<< HEAD
                        "reset_token_expires": datetime.utcnow()
                        + timedelta(minutes=15),
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

=======
                        "reset_token_expires": datetime.utcnow() + timedelta(minutes=15),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
>>>>>>> main
            return {"reset_token": reset_token}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def reset_password(self, reset_data: ForgotPasswordReset):
        try:
<<<<<<< HEAD
            user = await database.users.find_one(
                {
                    "email": reset_data.email,
                    "reset_token": reset_data.reset_token,
                    "reset_token_expires": {"$gt": datetime.utcnow()},
                }
            )

            if not user:
                raise HTTPException(
                    status_code=400, detail="Invalid or expired reset token"
                )

=======
            user = await database.users.find_one({
                "email": reset_data.email,
                "reset_token": reset_data.reset_token,
                "reset_token_expires": {"$gt": datetime.utcnow()}
            })
            
            if not user:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid or expired reset token"
                )
            
>>>>>>> main
            hashed_password = get_password_hash(reset_data.new_password)
            await database.users.update_one(
                {"email": reset_data.email},
                {
                    "$set": {
                        "hashed_password": hashed_password,
<<<<<<< HEAD
                        "updated_at": datetime.utcnow(),
                    },
                    "$unset": {"reset_token": "", "reset_token_expires": ""},
                },
            )

            return {"message": "Password reset successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
=======
                        "updated_at": datetime.utcnow()
                    },
                    "$unset": {
                        "reset_token": "",
                        "reset_token_expires": ""
                    }
                }
            )
            
            return {"message": "Password reset successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
>>>>>>> main

    async def create_user(self, user: UserCreate):
        try:
            existing_user = await self.get_user_by_email(user.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
<<<<<<< HEAD

=======
                        
>>>>>>> main
            # Create user data with preferences
            user_data = {
                "id": str(uuid.uuid4()),
                "email": user.email,
                "full_name": user.full_name,
                "hashed_password": get_password_hash(user.password),
                "is_active": True,
                "preferences": {
<<<<<<< HEAD
                    "cuisine_preferences": (
                        user.preferences.cuisine_preferences if user.preferences else []
                    ),
                    "dietary_restrictions": (
                        user.preferences.dietary_restrictions
                        if user.preferences
                        else []
                    ),
                    "allergies": user.preferences.allergies if user.preferences else [],
                    "cooking_skill_level": (
                        user.preferences.cooking_skill_level
                        if user.preferences
                        else "intermediate"
                    ),
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }

            result = await database.users.insert_one(user_data)
            if not result.inserted_id:
                raise HTTPException(status_code=500, detail="Failed to create user")

=======
                    "cuisine_preferences": user.preferences.cuisine_preferences if user.preferences else [],
                    "dietary_restrictions": user.preferences.dietary_restrictions if user.preferences else [],
                    "allergies": user.preferences.allergies if user.preferences else [],
                    "cooking_skill_level": user.preferences.cooking_skill_level if user.preferences else "intermediate"
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await database.users.insert_one(user_data)
            if not result.inserted_id:
                raise HTTPException(status_code=500, detail="Failed to create user")
            
>>>>>>> main
            created_user = await database.users.find_one({"_id": result.inserted_id})
            return UserInDB(**created_user)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
<<<<<<< HEAD
=======
        
>>>>>>> main

    async def update_user(self, user_id: str, updated_data: dict):
        try:
            # Ensure the user exists
            user = await database.users.find_one({"id": user_id})
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
<<<<<<< HEAD

=======
            
>>>>>>> main
            # Prepare updated fields
            updated_data["updated_at"] = datetime.utcnow()

            # Update the user document
            result = await database.users.update_one(
<<<<<<< HEAD
                {"id": user_id}, {"$set": updated_data}
            )

            if result.modified_count == 0:
                raise HTTPException(
                    status_code=500, detail="Failed to update user data"
                )

=======
                {"id": user_id},
                {"$set": updated_data}
            )
            
            if result.modified_count == 0:
                raise HTTPException(status_code=500, detail="Failed to update user data")
            
>>>>>>> main
            # Fetch the updated user data
            updated_user = await database.users.find_one({"id": user_id})
            return UserInDB(**updated_user)  # Return the updated user as UserInDB
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
<<<<<<< HEAD

=======
        
>>>>>>> main
    async def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email: str = payload.get("sub")
            if email is None:
                return None
            user = await self.get_user_by_email(email)
            return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
