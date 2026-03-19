
from app.core.db import get_db
from app.models.client import Client, Address
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

# !CHAR
router = APIRouter()

# !PYDANTIC


class ClientCreate(BaseModel):
    username: str
    phone: str
    city: str | None = None
    street: str | None = None
    house: str | None = None
    entrance: str | None = None


class AddressOut(BaseModel):
    id: int
    city: str | None = None
    street: str | None = None
    house: str | None = None
    entrance: str | None = None


class ClientGet(BaseModel):
    id: int
    username: str | None = None
    phone: str
    addresses: list[AddressOut] = []


# !ROUTES


@router.get("/client", tags=["Client"], response_model=list[ClientGet])
def list_clients(db: Session = Depends(get_db)):
    clients = db.execute(select(Client).options(
        selectinload(Client.addresses))).scalars().all()
    if not clients:
        return []
    else:
        return clients


@router.get("/client/{client_id}", tags=["Client"], response_model=ClientGet)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    client = db.execute(select(Client).where(Client.id == client_id).options(
        selectinload(Client.addresses))).scalar()
    if not client:
        raise HTTPException(404, "Client not found")
    return client


@router.get("/client/phone/{phone}", tags=["Client"], response_model=list[ClientGet])
def get_client_by_phone(phone: str, db: Session = Depends(get_db)):
    clients = db.execute(
        select(Client).options(selectinload(Client.addresses)).where(
            Client.phone.ilike(f"%{phone}%"))
    ).scalars().all()

    if not clients:
        return []

    return clients


@router.post("/client", tags=["Client"], response_model=ClientGet)
def create_client(data_client: ClientCreate, db: Session = Depends(get_db)):
    phone = format_phone_number(data_client.phone)
    client = Client(username=data_client.username, phone=phone)
    if data_client.city != "":
        client.addresses.append(
            Address(city=data_client.city, street=data_client.street if data_client.street != "" else None, house=data_client.house if data_client.house != "" else None, entrance=data_client.entrance if data_client.entrance != "" else None))
    try:
        db.add(client)
        db.commit()
        db.refresh(client)
        return client
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Phone already exists")


@router.patch("/client/{client_id}", tags=["Client"])
def update_client(client_id: int, username: str | None = None, phone: str | None = None, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(404, "Client not found")
    if username:
        client.username = username
    if phone:
        client.phone = format_phone_number(phone)
    try:
        db.add(client)
        db.commit()
        db.refresh(client)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Phone already exists")


@router.delete("/client/{client_id}", tags=["Client"])
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(404, "Client not found")
    db.delete(client)
    db.commit()


@router.post("/client/address", tags=["Client"])
def add_address_to_client(data_address: AddressOut , db: Session = Depends(get_db)):
    client = db.get(Client, data_address.id)
    if not client:
        raise HTTPException(404, "Client not found")
    address = Address(city=data_address.city, street=data_address.street, house=data_address.house, entrance=data_address.entrance)
    client.addresses.append(address)
    db.add(client)
    db.commit()
    db.refresh(client)


@router.delete("/client/{client_id}/address/{address_id}", tags=["Client"])
def delete_address_from_client(client_id: int, address_id: int, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(404, "Client not found")
    address = db.get(Address, address_id)
    if len(client.addresses) <= 1:
        # Выбрасываем ошибку вместо того, чтобы пытаться удалить
        raise HTTPException(400, "It last address does not exist")
    if not address or address not in client.addresses:
        raise HTTPException(404, "Address not found for this client")
    client.addresses.remove(address)
    db.delete(address)
    db.commit()


# !FUNCTIONS


def format_phone_number(phone: str) -> str:
    """Форматирует номер телефона в формат +7XXXXXXXXXX"""
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 11:
        formatted = f"+7{digits[1:4]}{digits[4:7]}{digits[7:9]}{digits[9:11]}"
        return formatted
    elif len(digits) == 10:
        formatted = f"+7{digits[0:3]}{digits[3:6]}{digits[6:8]}{digits[8:10]}"
        return formatted
    else:
        raise HTTPException(
            400, "Номер телефона должен содержать 10 или 11 цифр")
