from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from app.api.routes import auth, meal_planning, grocery, user, gmail
from app.api.dependencies import get_current_active_user
from app.db.database import database
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


# First Run: pip install -r requirements.txt
# Run this commad from the base folder i.e., dinewise-backend to start the backend
# uvicorn app.main:app --host localhost --port 8000

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database
    logger.info("Starting up...")
    try:
        if not await database.connect_to_database():
            logger.error("Failed to connect to the database")
            raise Exception("Failed to connect to MongoDB Atlas")
        logger.info("Successfully connected to MongoDB Atlas")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

    yield

    # Shutdown: Clean up resources
    logger.info("Shutting down...")
    await database.close_database_connection()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_base_url],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Public routes (no authentication required)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Protected routes (require authentication)
app.include_router(
    user.router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    meal_planning.router,
    prefix="/meal-planning",
    tags=["Meal Planning"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    grocery.router,
    prefix="/grocery",
    tags=["Grocery"],
    dependencies=[Depends(get_current_active_user)],
)

app.include_router(
    gmail.router,
    prefix="/gmail",
    tags=["Gmail"],
    dependencies=[Depends(get_current_active_user)],
)


@app.get("/")
async def root():
    return {"message": "Welcome to DineWise API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
