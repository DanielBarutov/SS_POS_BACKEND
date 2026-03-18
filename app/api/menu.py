
from datetime import datetime
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from app.core.db import get_db
from app.models.order import Order, OrderItem, OrderStatus
from pydantic import BaseModel
from app.models.product import Product
from app.models.client import Address, Client

# !CHAR
router = APIRouter()

# !PYDANTIC

class MenuGet(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int

# !ROUTES

@router.get("/menu", tags=["Menu"], response_model=list[MenuGet])
def get_menu(db: Session = Depends(get_db)):
    menu = db.execute(select(Product)).scalars().all()
    
    return menu
