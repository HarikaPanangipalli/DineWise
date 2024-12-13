"""
Database module for the DineWise application.

This module sets up a connection to MongoDB using the `motor` library and provides
references to collections used throughout the application.

Attributes:
    db_client (AsyncIOMotorClient): The MongoDB client instance.
    database (AsyncIOMotorDatabase): The main MongoDB database instance.
    users_collection (AsyncIOMotorCollection): Collection for storing user data.
    groceries_collection (AsyncIOMotorCollection): Collection for grocery data.
    meal_plans_collection (AsyncIOMotorCollection): Collection for meal plans.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging
import certifi

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    db = None

    async def connect_to_database(self):
        try:
            self.client = AsyncIOMotorClient(
                settings.mongodb_url,
                serverSelectionTimeoutMS=5000,
                ssl=True,
                tlsCAFile=certifi.where(),
            )
            self.db = self.client[settings.database_name]

            # Initialize collections
            self.users = self.db.users
            self.meal_plans = self.db.meal_plans
            self.groceries = self.db.groceries

            # Verify the connection
            await self.client.admin.command("ping")
            logger.info("Successfully connected to MongoDB Atlas!")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB Atlas: {str(e)}")
            return False

    async def close_database_connection(self):
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB Atlas connection")


database = Database()
