from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class GroceryBase(BaseModel):
    items: List[str]

class GroceryCreate(GroceryBase):
    date: date

    class Config:
        from_attributes = True

class GroceryResponse(GroceryBase):
    id: str
    user_id: str
    date: date

    class Config:
        from_attributes = True

class GroceryUpdate(BaseModel):
    items: List[str]

    class Config:
        from_attributes = True

class GroceryInDB(BaseModel):
    id: str
    user_id: str
    items: List[dict]
    first_email_date: datetime
    last_email_date: datetime
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True

class GroceryItem(BaseModel):
    item_name: str
    quantity: int
    price: Optional[float] = None

class GroceryListResponse(BaseModel):
    id: str
    user_id: str
    items: List[GroceryItem]
    source_emails: List[str]
    extraction_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class GroceryListsResponse(BaseModel):
    status: str
    total_lists: int
    lists: List[GroceryListResponse]

    class Config:
        from_attributes = True