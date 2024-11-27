"""
Gmail Routes

Defines FastAPI routes for Gmail-related operations.

Routes:
- fetch_emails: Retrieves emails based on a user-provided query.
"""

from fastapi import APIRouter, Depends, HTTPException
from app.services.gmail_service import GmailService
from app.services.grocery_service import GroceryService
from app.schemas.user import UserResponse
from app.api.dependencies import get_current_user
from datetime import datetime


router = APIRouter()
gmail_service = GmailService()
grocery_service = GroceryService()

@router.get("/extract-groceries")
async def extract_and_store_groceries(
    days: int = 30,
    current_user: UserResponse = Depends(get_current_user)
):
    """Extract groceries from emails and store consolidated list"""
    try:
        # First authenticate and fetch emails
        await gmail_service.initialize_service(current_user.id)

        # Get last email date from database
        last_email_date_extracted = await grocery_service.get_last_email_date(current_user.id)
        if last_email_date_extracted:
            last_email_date_extracted = last_email_date_extracted.strftime("%Y/%m/%dT%H:%M:%S")
        
        # Fetch emails with grocery orders
        query = "from:vikramaditya549@gmail.com"
        emails, first_email_date, last_email_date = await gmail_service.fetch_emails(query=query, last_email_date_extracted=last_email_date_extracted)
        if not emails:
            return {
                "message": "No grocery emails found",
                "total_emails": 0
            }
        
        # Store consolidated groceries
        consolidated_list = await grocery_service.store_consolidated_groceries(
            user_id=current_user.id,
            extracted_emails=emails, 
            first_email_date=first_email_date,
            last_email_date=last_email_date
        )
        
        return {
            "message": "Groceries extracted and stored successfully",
            "total_emails_processed": len(emails),
            "extraction_date": consolidated_list["extraction_date"],
            "total_items": len(consolidated_list["items"]),
            "grocery_list_id": consolidated_list["id"],
            "first_email_date": first_email_date,
            "last_email_date": last_email_date
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process groceries: {str(e)}"
        )

@router.get("/grocery-lists")
async def get_user_grocery_lists(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get all grocery lists for the user"""
    try:
        lists = await grocery_service.get_user_grocery_lists(current_user.id)
        return {
            "status": "success",
            "total_lists": len(lists),
            "lists": lists
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    


@router.get("/auth")
async def gmail_auth(current_user: UserResponse = Depends(get_current_user)):
    """Initialize Gmail authentication"""
    try:
        await gmail_service.initialize_service(current_user.id)
        return {"message": "Gmail service initialized successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize Gmail service: {str(e)}"
        )