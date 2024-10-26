# Meal Plans Schema
meal_plans_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["generation_date", "meal_plan"],
        "properties": {
            "meal_plan_id": {"bsonType": "string"},
            "user_id": {"bsonType": "string"},
            "generation_date": {"bsonType": "date"},
            "meal_plan": {"bsonType": "string"},
            "status": {"bsonType": "string"},
            "week_starting": {"bsonType": "date"},
            "nutritional_info": {"bsonType": "object"},
        },
    }
}
