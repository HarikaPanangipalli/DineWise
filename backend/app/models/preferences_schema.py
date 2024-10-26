# Preferences Schema
preferences_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id"],
        "properties": {
            "pref_id": {"bsonType": "string"},
            "user_id": {"bsonType": "string"},
            "default_cuisine_type": {"bsonType": "string"},
            "dietary_restrictions": {"bsonType": "array"},
            "allergies": {"bsonType": "array"},
            "cooking_skill_level": {"bsonType": "string"},
            "preferred_meal_times": {"bsonType": "object"},
        },
    }
}
