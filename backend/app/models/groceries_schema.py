# Groceries Schema
groceries_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["item_name", "quantity", "date_synced"],
        "properties": {
            "grocery_id": {"bsonType": "string"},
            "item_name": {"bsonType": "string"},
            "quantity": {"bsonType": "int"},
            "date_synced": {"bsonType": "date"},
            "category": {"bsonType": "string"},
            "unit": {"bsonType": "string"},
        },
    }
}
