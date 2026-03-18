

from datetime import datetime
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from app.core.db import get_db
from app.models.order import Order, OrderItem, OrderStatus
from pydantic import BaseModel, validator
from app.models.product import Product
from app.models.client import Address, Client
from enum import Enum
from typing import Optional

# !CHAR
router = APIRouter()

# !PYDANTIC

class PaymentType(str, Enum):
    cash = "cash"
    card = "card"

class OrderItemCreate(BaseModel):
    product_id: int
    name: str
    price_retail: float
    qty: int
    


class OrderCreate(BaseModel):
    id: int | None = None
    client_id: int
    address_id: int | None = None
    status: OrderStatus
    payment_type: Optional[str] = None
    sum_order: float | None = None
    comment: str | None = None
    devices: int | None = None

    @validator('payment_type', pre=True)
    def validate_payment_type(cls, v):
        """Конвертирует Enum в строку"""
        if v is None:
            return None
        if isinstance(v, PaymentType):
            return v.value
        return str(v)

class OrderPatch(BaseModel):
    client_id: Optional[int] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    address_id: Optional[int] = None
    address: Optional[str] = None
    status: Optional[str] = None
    payment_type: Optional[str] = None  # строка
    comment: Optional[str] = None
    devices: Optional[int] = None
    sum_order: Optional[float] = None
    
    @validator('status', 'payment_type', pre=True)
    def validate_enum_values(cls, v):
        """Принимает как строки, так и Enum объекты"""
        if v is None:
            return None
        # Если пришел Enum, берем его значение
        if hasattr(v, 'value'):
            return v.value
        # Если строка, возвращаем как есть
        return str(v)

class OrderItemPatch(BaseModel):
    product_id: int | None = None
    name: str | None = None
    price_retail: float | None = None
    qty: int | None = None

class OrderGet(BaseModel):
    id: int
    client_id: int
    username: str
    phone: str
    address_id: int | None = None
    address: str | None = None
    status: OrderStatus
    payment_type: PaymentType | None = None
    created_at: str
    comment: str | None = None
    items: list[OrderItemCreate]
    sum_order: float | None = None
    devices: int | None = None


# !ROUTES


@router.get("/orders", tags=["Order"], response_model=list[OrderGet])
def get_orders(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).options(
        selectinload(Order.items))).scalars().all()
    client_usernames = {client.id: client.username for client in db.execute(select(Client)).scalars().all()}
    client_phones = {client.id: client.phone for client in db.execute(select(Client)).scalars().all()}
    address_dict = {address.id: f"{address.city}, {address.street}, д. {address.house}, п. {address.entrance}" for address in db.execute(select(Address)).scalars().all()}
    orders_with_details = []
    for order in orders:
        order_data = OrderGet(
            id=order.id,
            client_id=order.client_id,
            username=client_usernames.get(order.client_id, "Unknown"),
            phone=client_phones.get(order.client_id, "Unknown"),
            address_id=order.address_id,
            address=address_dict.get(order.address_id, "Unknown"),
            status=order.status,
            payment_type=order.payment_type,
            comment=order.comment,
            created_at=order.created_at.strftime("%d.%m %H:%M"),
            items=[OrderItemCreate(product_id=item.product_id, name=item.name, price_retail=item.price_retail, qty=item.qty) for item in order.items],
            sum_order=order.sum_order,
            devices=order.devices
        )
        orders_with_details.append(order_data)

    if not orders:
        raise HTTPException(404, "Orders not found")

    return orders_with_details


@router.get("/order/{order_id}", tags=["Order"], response_model=OrderGet)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.execute(select(Order).where(Order.id == order_id).options(
        selectinload(Order.items))).scalar()
    client_usernames = {client.id: client.username for client in db.execute(select(Client)).scalars().all()}
    client_phones = {client.id: client.phone for client in db.execute(select(Client)).scalars().all()}
    address_dict = {address.id: f"{address.city}, {address.street}, д. {address.house}, п. {address.entrance}" for address in db.execute(select(Address)).scalars().all()}
    if not order:
        raise HTTPException(404, "Order not found")
    
    order_data = OrderGet(
        id=order.id,
        client_id=order.client_id,
        username=client_usernames.get(order.client_id, "Unknown"),
        phone=client_phones.get(order.client_id, "Unknown"),
        address_id=order.address_id,
        address=address_dict.get(order.address_id, "Unknown"),
        status=order.status,
        payment_type=order.payment_type,
        created_at=order.created_at.strftime("%X"),
        comment=order.comment,
        items=[OrderItemCreate(product_id=item.product_id, name=item.name, price_retail=item.price_retail, qty=item.qty) for item in order.items],
        sum_order=order.sum_order,
        devices=order.devices
        )
        
    return order_data


@router.post("/order", tags=["Order"])
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    if db.execute(select(Client).where(Client.id == order_data.client_id)).scalar() is None:
        raise HTTPException(400, "Client not found")
   
   
    new_order = Order(
        id=None,
        client_id=order_data.client_id,
        address_id=order_data.address_id,
        status=order_data.status,
        payment_type=order_data.payment_type,
        sum_order=order_data.sum_order,
        comment=order_data.comment,
        devices=order_data.devices
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.post("/order/{order_id}/item", tags=["Order"])
def add_order_item(order_id: int, item_data: OrderItemCreate, db: Session = Depends(get_db)):
    order = db.execute(select(Order).where(
        Order.id == order_id)).scalar_one_or_none()
    if not order:
        raise HTTPException(404, "Order not found")

    product = db.execute(select(Product).where(
        Product.id == item_data.product_id)).scalar_one_or_none()
    if not product:
        raise HTTPException(404, "Product not found")

        
    item = db.execute(
        select(OrderItem).where(
            OrderItem.order_id == order_id,
            OrderItem.product_id == item_data.product_id,
            OrderItem.name == item_data.name,
            OrderItem.price_retail == item_data.price_retail,
            
        )
    ).scalar_one_or_none()


    if item:
        item.qty += item_data.qty
    else:
        item = OrderItem(order_id=order_id,
                         product_id=item_data.product_id, name=item_data.name, price_retail=item_data.price_retail, qty=item_data.qty)
        db.add(item)

    db.commit()
    db.refresh(order)
    return order


@router.patch("/order/{order_id}/status", tags=["Order"])
def update_order_status(order_id: int, status: OrderStatus, db: Session = Depends(get_db)):
    order = db.execute(select(Order).where(Order.id == order_id)).scalar()
    if not order:
        raise HTTPException(404, "Order not found")

    order.status = status
    db.commit()
    db.refresh(order)
    return order.status


@router.delete("/order/{order_id}", tags=["Order"])
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.execute(select(Order).where(Order.id == order_id)).scalar()
    if not order:
        raise HTTPException(404, "Order not found")

    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}


@router.patch("/order/{order_id}/item/{product_id}", tags=["Order"])
def update_order_item(order_id: int, product_id: int, item_data: OrderItemPatch, db: Session = Depends(get_db)):
    item = db.execute(select(OrderItem).where(
        OrderItem.order_id == order_id, OrderItem.product_id == product_id)).scalar()
    if not item:
        raise HTTPException(404, "Order item not found")
    
    if item_data.name is not None:
        item.name = item_data.name
    if item_data.qty is not None:
        item.qty = item_data.qty
    if item_data.price_retail is not None:
        item.price_retail = item_data.price_retail
    product_price = db.execute(select(Product.price_retail).where(
        Product.id == item_data.product_id)).scalar()
    sum_change = (product_price or 0) * item_data.qty
    order = db.execute(select(Order).where(
        Order.id == order_id)).scalar()
    order.sum_order = (order.sum_order or 0) - sum_change  # type: ignore
    
    if item.qty <= 0:
        db.delete(item)
        db.commit()
        return {"message": "Item deleted"} # Выходим, не обновляя
    else:
        db.commit()
        db.refresh(item)
        return item # type: ignore

@router.patch("/order/{order_id}", tags=["Order"])
def update_order(order_id: int, order_data: OrderPatch, db: Session = Depends(get_db)):
  
    # Находим заказ
    order = db.execute(select(Order).where(Order.id == order_id)).scalar()
    if not order:
        raise HTTPException(404, "Order not found")
   
    # Получаем данные для обновления
    update_data = order_data.dict(exclude_unset=True)
    
    # Обновляем поля
    for field, value in update_data.items():
        if value is not None:
            setattr(order, field, value)
            
    db.commit()
    db.refresh(order)
    
    return order

@router.delete("/order/{order_id}/item/{product_id}", tags=["Order"])
def delete_order_item(order_id: int, product_id: int, db: Session = Depends(get_db)):
    item = db.execute(select(OrderItem).where(
        OrderItem.order_id == order_id, OrderItem.product_id == product_id)).scalar()
    if not item:
        raise HTTPException(404, "Order item not found")

    db.delete(item)
    db.commit()
    return {"detail": "Order item deleted successfully"}
# !FUNCTIONS
