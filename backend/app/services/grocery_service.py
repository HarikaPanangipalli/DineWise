from app.db.database import database
from datetime import datetime
import uuid
import re
from bson import ObjectId
from fastapi import HTTPException



class GroceryService:
    async def extract_groceries_from_emails(self, emails: list) -> list:
        """Extract grocery items from emails"""
        try:
            all_items = []
            
            for email in emails:
                # Make sure email is a dictionary and has a body
                if isinstance(email, dict) and 'body' in email:
                    body = email['body']
                    
                    # Look for the items section
                    start_marker = "Ordered items"
                    end_marker = "Subtotal"
                    
                    start_idx = body.find(start_marker)
                    end_idx = body.find(end_marker)
                    
                    if start_idx != -1 and end_idx != -1:
                        items_section = body[start_idx:end_idx]
                        
                        # Pattern to match item name, quantity and price
                        pattern = r'([^\n]+?)\n\s*(\d+)\s*\$(\d+\.\d{2})'
                        
                        # Find all matches
                        matches = re.finditer(pattern, items_section)
                        
                        for match in matches:
                            item = {
                                'item_name': match.group(1).strip(),
                                'quantity': int(match.group(2)),
                                'price': float(match.group(3))
                            }
                            all_items.append(item)
            
            return all_items
            
        except Exception as e:
            print(f"Error extracting groceries: {str(e)}")
            raise Exception(f"Failed to extract groceries: {str(e)}")

    async def store_consolidated_groceries(self, user_id: str, extracted_emails: list, first_email_date: datetime, last_email_date: datetime) -> dict:
        """Store consolidated groceries from multiple emails"""
        try:
            # Extract items from emails
            items = await self.extract_groceries_from_emails(extracted_emails)
            print(user_id)
            
            # Consolidate items
            consolidated_items = {}
            for item in items:
                item_name = item['item_name']
                if item_name in consolidated_items:
                    consolidated_items[item_name]['quantity'] += item['quantity']
                    # consolidated_items[item_name]['total'] = (
                    #     consolidated_items[item_name]['quantity'] * 
                    #     consolidated_items[item_name]['price']
                    # )
                else:
                    consolidated_items[item_name] = {
                        'item_name': item_name,
                        'quantity': item['quantity'],
                        'price': item['price'],
                        # 'total': item['quantity'] * item['price']
                    }
            
            # Create grocery list document
            grocery_data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "items": list(consolidated_items.values()),
                "source_emails": [
                    email['id'] if isinstance(email, dict) and 'id' in email else str(uuid.uuid4())
                    for email in extracted_emails
                ],
                "extraction_date": datetime.utcnow(),
                "first_email_date": first_email_date,
                "last_email_date": last_email_date,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Store in database
            result = await database.db.groceries.insert_one(grocery_data)
            if not result.inserted_id:
                raise Exception("Failed to store grocery list")
            
            return grocery_data
            
        except Exception as e:
            print(f"Error storing groceries: {str(e)}")
            raise Exception(f"Failed to store consolidated groceries: {str(e)}")

    async def get_user_grocery_lists(self, user_id: str) -> list:
        """Get all grocery lists for a user"""
        try:
            cursor = database.db.groceries.find({"user_id": user_id})
            grocery_lists = await cursor.to_list(length=None)
            
            # Convert ObjectId to string and format the response
            formatted_lists = []
            for grocery in grocery_lists:
                formatted_grocery = {
                    "id": str(grocery["_id"]),  # Convert ObjectId to string
                    "user_id": grocery["user_id"],
                    "items": grocery.get("items", []),
                    "source_emails": grocery.get("source_emails", []),
                    "extraction_date": grocery.get("extraction_date"),
                    "created_at": grocery.get("created_at"),
                    "updated_at": grocery.get("updated_at")
                }
                formatted_lists.append(formatted_grocery)
            
            return formatted_lists
            
        except Exception as e:
            print(f"Error fetching grocery lists: {str(e)}")
            raise Exception(f"Failed to fetch grocery lists: {str(e)}")
        
    async def get_last_email_date(self, user_id: str) -> datetime:
        """Get the last email date from the most recent grocery list"""
        try:
            latest_grocery = await database.db.groceries.find_one(
                {"user_id": user_id},
                sort=[("last_email_date", -1)]
            )
            if latest_grocery and 'last_email_date' in latest_grocery:
                return latest_grocery['last_email_date']
            return None
        except Exception as e:
            print(f"Error fetching last email date: {str(e)}")
            return None
        
    async def get_grocery_by_id(self, grocery_id: str, user_id: str) -> dict:
        """Get grocery list by ID"""
        try:
            # Find grocery list by ID and user_id
            grocery = await database.db.groceries.find_one({
                "id": grocery_id,
                "user_id": user_id
            })
            
            if not grocery:
                raise HTTPException(
                    status_code=404,
                    detail="Grocery list not found"
                )

            # Format response
            return {
                "id": str(grocery["_id"]),
                "user_id": grocery["user_id"],
                "items": grocery.get("items", []),
                "first_email_date": grocery.get("first_email_date"),
                "last_email_date": grocery.get("last_email_date"),
                "created_at": grocery.get("created_at"),
                "updated_at": grocery.get("updated_at")
            }
            
        except Exception as e:
            print(f"Error fetching grocery list: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch grocery list: {str(e)}"
            )
        
    async def update_grocery_list(self, grocery_id: str, user_id: str, new_item: dict) -> dict:
        """Add new item to existing grocery list"""
        try:
            # Find the existing grocery list
            grocery = await database.db.groceries.find_one({
                "id": grocery_id,
                "user_id": user_id
            })
            
            if not grocery:
                raise HTTPException(
                    status_code=404,
                    detail="Grocery list not found"
                )

            # Add the new item to the items array
            updated_grocery = await database.db.groceries.find_one_and_update(
                {"id": grocery_id},
                {
                    "$push": {"items": new_item},
                    "$set": {"updated_at": datetime.utcnow()}
                },
                return_document=True
            )

            # Format response
            return {
                "id": str(updated_grocery["_id"]),
                "user_id": updated_grocery["user_id"],
                "items": updated_grocery.get("items", []),
                "created_at": updated_grocery.get("created_at"),
                "updated_at": updated_grocery.get("updated_at")
            }
            
        except Exception as e:
            print(f"Error updating grocery list: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update grocery list: {str(e)}"
            )
        

    async def delete_grocery_item(self, grocery_id: str, item_index: int, user_id: str) -> dict:
        """Delete an item from grocery list"""
        try:
            # Find the grocery list and verify ownership
            grocery = await database.db.groceries.find_one({
                "id": grocery_id,
                "user_id": user_id
            })
            
            if not grocery:
                raise HTTPException(
                    status_code=404,
                    detail="Grocery list not found"
                )

            # Remove the item at the specified index
            updated_grocery = await database.db.groceries.find_one_and_update(
                {"id": grocery_id},
                {
                    "$unset": {f"items.{item_index}": 1},
                    "$set": {"updated_at": datetime.utcnow()}
                },
                return_document=True
            )

            # Pull null values created by unset
            updated_grocery = await database.db.groceries.find_one_and_update(
                {"id": grocery_id},
                {
                    "$pull": {"items": None}
                },
                return_document=True
            )

            return {
                "id": str(updated_grocery["_id"]),
                "items": updated_grocery.get("items", []),
                "updated_at": updated_grocery.get("updated_at")
            }
            
        except Exception as e:
            print(f"Error deleting grocery item: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete grocery item: {str(e)}"
            )
