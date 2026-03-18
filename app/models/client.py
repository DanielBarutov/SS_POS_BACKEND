from sqlalchemy import String, ForeignKey
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from datetime import datetime
from sqlalchemy import func, DateTime


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(25), unique=False, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="client",
        cascade="all, delete-orphan",
    )


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False)
    city: Mapped[str] = mapped_column(String(60), nullable=True)
    street: Mapped[str] = mapped_column(String(60), nullable=True)
    house: Mapped[str] = mapped_column(String(60), nullable=True)
    entrance: Mapped[str] = mapped_column(String(60), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    client: Mapped["Client"] = relationship(
        "Client",
        back_populates="addresses",
    )
