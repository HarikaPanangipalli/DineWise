# User Profiles Schema
user_profiles_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_name", "password", "created_time", "is_ecommerce_linked"],
        "properties": {
            "user_id": {"bsonType": "string"},
            "user_name": {"bsonType": "string"},
            "password": {"bsonType": "string"},
            "email": {"bsonType": "string"},
            "is_ecommerce_linked": {"bsonType": "bool"},
            "auth_token_for_gmail": {"bsonType": "string"},
            "created_time": {"bsonType": "date"},
            "last_login": {"bsonType": "date"},
            "profile_status": {"bsonType": "string"},
            "notification_preferences": {"bsonType": "object"},
        },
    }
}
