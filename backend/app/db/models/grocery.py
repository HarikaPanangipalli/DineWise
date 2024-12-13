from datetime import datetime
from typing import List

class GroceryInDB:
    """
    Represents a grocery item stored in the database.

    Attributes:
        id (str): Unique identifier for the grocery entry.
        user_id (str): Identifier for the user who owns the grocery list.
        items (List[dict]): List of grocery items with details (e.g., name, quantity).
        source_emails (List[str]): Email IDs from which items were extracted.
        extraction_date (datetime): Date the groceries were extracted from emails.
        created_at (datetime): Timestamp when the entry was created.
        updated_at (datetime): Timestamp when the entry was last updated.
    """
    def __init__(
        self,
        id: str,
        user_id: str,
        items: List[dict],  # List of items with details
        source_emails: List[str],  # List of email IDs from which items were extracted
        extraction_date: datetime,
        created_at: datetime = datetime.utcnow(),
        updated_at: datetime = datetime.utcnow(),
    ):
        self.id = id
        self.user_id = user_id
        self.items = items
        self.source_emails = source_emails
        self.extraction_date = extraction_date
        self.created_at = created_at
        self.updated_at = updated_at
