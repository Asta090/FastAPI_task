from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionDep
import models
import schemas
from sqlmodel import select
from e_utility import send_order_email
from typing import Annotated, List
from oauth2 import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.get("/", response_model=List[schemas.OrderOut])
async def get_orders(
    session: SessionDep,
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    # Get all orders for the current user
    orders = session.exec(
        select(models.Order).where(models.Order.buyer_id == current_user.user_id)
    ).all()
    return orders

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderOut)
async def place_order(
    request: schemas.order_create,
    session: SessionDep,
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    db_order = models.Order(
        product=request.product,
        quantity=request.quantity,
        address=request.address,
        buyer_id=current_user.user_id,  # Changed from id to user_id
        status="pending" 
    )
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    
    # Send email notification
    await send_order_email(current_user.email, db_order)
    return db_order

@router.patch("/{order_id}/status", response_model=schemas.OrderOut)
async def update_order_status(
    order_id: int,
    status_update: schemas.order_status_update,
    session: SessionDep,
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    order = session.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.buyer_id != current_user.user_id:  # Changed from id to user_id
        raise HTTPException(status_code=403, detail="Not authorized to update this order")
    
    order.status = status_update.status
    session.add(order)
    session.commit()
    session.refresh(order)
    
    # Send status update email
    await send_order_email(current_user.email, order)
    return order