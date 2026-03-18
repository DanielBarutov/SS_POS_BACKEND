from sqlalchemy import ForeignKey, String, Integer, Enum, Float
import enum
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from datetime import datetime
from sqlalchemy import func, DateTime


class OrderStatus(str, enum.Enum):
    cooking = "cooking"
    completed_not_paid = "completed_not_paid"
    completed_paid = "completed_paid"
    in_delivery = "in_delivery"
    ending = "ending"
    cancelled = "cancelled"

class PaymentType(str, enum.Enum):
    cash = "cash"
    card = "card"
    

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(
        ForeignKey("addresses.id"), nullable=True)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.cooking)
    payment_type: Mapped[PaymentType] = mapped_column(
        Enum(PaymentType), nullable=True)
    sum_order: Mapped[float | None] = mapped_column(nullable=True)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    devices: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"
    order_id: Mapped[int] = mapped_column(ForeignKey(
        "orders.id", ondelete="CASCADE"), primary_key=True)
    
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price_retail: Mapped[float] = mapped_column(Float, nullable=False)
    qty: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    order: Mapped["Order"] = relationship("Order", back_populates="items")
