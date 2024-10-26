# app/database.py

from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
import os
from app.models.groceries_schema import groceries_schema
from app.models.preferences_schema import preferences_schema
from app.models.meal_plans_schema import meal_plans_schema
from app.models.user_profiles_schema import user_profiles_schema

load_dotenv()


class Database:
    def __init__(self):
        self.client = MongoClient(
            os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        )
        self.db = self.client["dinewise"]
        self.setup_collections()

    def setup_collections(self):
        # Setup Groceries
        groceries = self.db["groceries"]
        groceries.create_index([("grocery_id", ASCENDING)], unique=True)
        groceries.create_index([("item_name", ASCENDING)])

        # Setup Preferences
        preferences = self.db["preferences"]
        preferences.create_index([("pref_id", ASCENDING)], unique=True)
        preferences.create_index([("user_id", ASCENDING)], unique=True)

        # Setup Meal Plans
        meal_plans = self.db["meal_plans"]
        meal_plans.create_index([("meal_plan_id", ASCENDING)], unique=True)

        # Setup User Profiles
        user_profiles = self.db["user_profiles"]
        user_profiles.create_index([("user_id", ASCENDING)], unique=True)
        user_profiles.create_index([("user_name", ASCENDING)], unique=True)

        # Apply validators
        self.db.command("collMod", "groceries", validator=groceries_schema)
        self.db.command("collMod", "preferences", validator=preferences_schema)
        self.db.command("collMod", "meal_plans", validator=meal_plans_schema)
        self.db.command("collMod", "user_profiles", validator=user_profiles_schema)

    def get_collection(self, collection_name):
        return self.db[collection_name]
