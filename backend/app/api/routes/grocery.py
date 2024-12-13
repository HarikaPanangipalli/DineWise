from fastapi import APIRouter, Depends, HTTPException
from app.schemas.grocery import GroceryCreate, GroceryResponse
from app.services.grocery_service import GroceryService
from app.schemas.user import UserResponse
from app.api.dependencies import get_current_user

router = APIRouter()
grocery_service = GroceryService()


@router.post("/grocery", response_model=GroceryResponse)
async def create_grocery_list(
    grocery: GroceryCreate, current_user: UserResponse = Depends(get_current_user)
):
    return await grocery_service.create_grocery_list(current_user.id, grocery)


@router.get("/grocery/{date}", response_model=GroceryResponse)
async def get_grocery_list(
    date: str, current_user: UserResponse = Depends(get_current_user)
):
    return await grocery_service.get_grocery_list(current_user.id, date)


@router.get("/{grocery_id}")
async def get_grocery_by_id(
    grocery_id: str, current_user: UserResponse = Depends(get_current_user)
):
    """Get grocery list by ID"""
    try:
        return await grocery_service.get_grocery_by_id(grocery_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{grocery_id}/items")
async def add_grocery_item(
    grocery_id: str, item: dict, current_user: UserResponse = Depends(get_current_user)
):
    """Add new item to grocery list"""
    try:
        return await grocery_service.update_grocery_list(
            grocery_id=grocery_id, user_id=current_user.id, new_item=item
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{grocery_id}/items/{item_index}")
async def delete_grocery_item(
    grocery_id: str,
    item_index: int,
    current_user: UserResponse = Depends(get_current_user),
):
    """Delete item from grocery list"""
    try:
        return await grocery_service.delete_grocery_item(
            grocery_id=grocery_id, item_index=item_index, user_id=current_user.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
