from operator import and_
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload, joinedload
from app.core.db import get_db
from app.models.product import Product, Category
from pydantic import BaseModel
from app.models.order import Order
from datetime import date, datetime, timedelta, timezone
from app.models.order import OrderStatus
from app.models.order import OrderItem
from sqlalchemy import func
from app.models.order import PaymentType



# !CHAR
router = APIRouter()

now = datetime.now(timezone.utc)
today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

# !PYDANTIC
class TopPositions(BaseModel):
    name: str
    total_qty: int

class AnalyticsResponse(BaseModel):
    top_by_qty: list[TopPositions]
    top_by_frequency: list[TopPositions]

@router.get("/stats/income24h", tags=["Stats"])
def get_income24h(db: Session = Depends(get_db)):
    income24h = db.execute(select(Order).where(Order.created_at >= datetime.now() - timedelta(hours=24), Order.status == OrderStatus.ending)).scalars().all()
    return {
        sum(order.sum_order for order in income24h)
    }

@router.get("/stats/income7d", tags=["Stats"])
def get_income7d(db: Session = Depends(get_db)):
    income7d = db.execute(select(Order).where(Order.created_at >= datetime.now() - timedelta(days=7), Order.status == OrderStatus.ending)).scalars().all()
    return {
        sum(order.sum_order for order in income7d)
    }

@router.get("/stats/income30d", tags=["Stats"])
def get_income30d(db: Session = Depends(get_db)):
    income30d = db.execute(select(Order).where(Order.created_at >= datetime.now() - timedelta(days=30), Order.status == OrderStatus.ending)).scalars().all()
    return {
        sum(order.sum_order for order in income30d)
    }

@router.get("/stats/average_order_price", tags=["Stats"])
def get_average_order_price(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).where(Order.status == OrderStatus.ending)).scalars().all()
    return {
        sum(order.sum_order for order in orders) / len(orders)
    }

@router.get("/stats/average_order_price_24h", tags=["Stats"])
def get_average_order_price_24h(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).where(Order.created_at >= datetime.now() - timedelta(hours=24), Order.status == OrderStatus.ending)).scalars().all()
    return {
        sum(order.sum_order for order in orders) / len(orders)
    }

@router.get("/stats/average_order_price_7d", tags=["Stats"])
def get_average_order_price_7d(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).where(Order.created_at >= datetime.now() - timedelta(days=7), Order.status == OrderStatus.ending)).scalars().all()
    return {
        sum(order.sum_order for order in orders) / len(orders)
    }

@router.get("/stats/average_order_price_30d", tags=["Stats"])
def get_average_order_price_30d(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).where(Order.created_at >= datetime.now() - timedelta(days=30), Order.status == OrderStatus.ending)).scalars().all()
    return {
        sum(order.sum_order for order in orders) / len(orders)
    }

@router.get("/stats/total_orders", tags=["Stats"])
def get_total_orders(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).where(Order.status == OrderStatus.ending)).scalars().all()
    return len(orders)

@router.get("/stats/total_orders_24h", tags=["Stats"]) # !TODO: ИСПРАВЛЕНИЕ
def get_total_orders_24h(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).where(Order.created_at >= today_start)).scalars().all()
    return len(orders)

@router.get("/stats/total_orders_7d", tags=["Stats"])
def get_total_orders_7d(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).where(Order.created_at >= datetime.now() - timedelta(days=7), Order.status == OrderStatus.ending)).scalars().all()
    return len(orders)

@router.get("/stats/total_orders_30d", tags=["Stats"])
def get_total_orders_30d(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).where(Order.created_at >= datetime.now() - timedelta(days=30), Order.status == OrderStatus.ending)).scalars().all()
    return len(orders)

@router.get("/stats/top_positions", tags=["Stats"])
def get_popular_products(db: Session = Depends(get_db)):
    # 1. Топ по общему количеству штук (SUM)
    res_positions = db.execute(
        select(Product.name, func.sum(OrderItem.qty))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.qty).desc()) # desc для топа
        .limit(10)
    ).all()

    # 2. Топ по частоте в заказах (COUNT)
    res_count = db.execute(
        select(Product.name, func.count(OrderItem.order_id))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.count(OrderItem.order_id).desc())
        .limit(10)
    ).all()

    # Преобразуем кортежи в список объектов, подходящих под схему
    return {
        "top_by_qty": [
            {"name": row[0], "value": row[1]} for row in res_positions
        ],
        "top_by_frequency": [
            {"name": row[0], "value": row[1]} for row in res_count
        ]
    }

@router.get("/stats/top_positions_24h", tags=["Stats"])
def get_top_positions_qty_24h(db: Session = Depends(get_db)):
    res_positions = db.execute(
        select(Product.name, func.sum(OrderItem.qty))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.qty).desc())
        .limit(10)
    ).all()
    return {
        
            {"name": row[0], "value": row[1]} for row in res_positions
        }

@router.get("/stats/top_positions_frequency_24h", tags=["Stats"])
def get_top_positions_frequency_24h(db: Session = Depends(get_db)):
    res_count = db.execute(
        select(Product.name, func.count(OrderItem.order_id))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.count(OrderItem.order_id).desc())
        .limit(10)
    ).all()
    return {
        
            {"name": row[0], "value": row[1]} for row in res_count
        }

@router.get("/stats/top_positions_7d", tags=["Stats"])
def get_top_positions_qty_7d(db: Session = Depends(get_db)):
    res_positions = db.execute(
        select(Product.name, func.sum(OrderItem.qty))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.qty).desc())
        .limit(10)
    ).all()
    return {
        
            {"name": row[0], "value": row[1]} for row in res_positions
        }

@router.get("/stats/top_positions_frequency_7d", tags=["Stats"])
def get_top_positions_frequency_7d(db: Session = Depends(get_db)):
    res_count = db.execute(
        select(Product.name, func.count(OrderItem.order_id))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.count(OrderItem.order_id).desc())
        .limit(10)
    ).all()
    return {
        
            {"name": row[0], "value": row[1]} for row in res_count
        }

@router.get("/stats/top_positions_30d", tags=["Stats"])
def get_top_positions_qty_30d(db: Session = Depends(get_db)):
    res_positions = db.execute(
        select(Product.name, func.sum(OrderItem.qty))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.qty).desc())
        .limit(10)
    ).all()
    return {
        
            {"name": row[0], "value": row[1]} for row in res_positions
        }  

@router.get("/stats/top_positions_frequency_30d", tags=["Stats"])
def get_top_positions_frequency_30d(db: Session = Depends(get_db)):
    res_count = db.execute(
        select(Product.name, func.count(OrderItem.order_id))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.count(OrderItem.order_id).desc())
        .limit(10)
    ).all()
    return {
          
            {"name": row[0], "value": row[1]} for row in res_count
        }

@router.get("/stats/listsell_positions_today", tags=["Stats"])
def get_lists_positions_today(db: Session = Depends(get_db)):
    res_positions = db.execute(
        select(
            Order.id, 
            Order.created_at, 
            OrderItem.name, 
            func.sum(OrderItem.qty).label('total_qty'), 
            func.sum(OrderItem.price_retail * OrderItem.qty).label('total_sum')
        )
        .join(OrderItem)
        .where(
            Order.status == "ending",
            Order.created_at >= today_start
        )
        .group_by(Order.id, Order.created_at, OrderItem.name)
    ).all()
    result = []
    aggregated = {}

    for row in res_positions:
        name = row[2]
        value = row[3]
        sum_price = row[4]
        
        if name in aggregated:
            aggregated[name]["value"] += value
            aggregated[name]["sum_price"] += sum_price
        else:
            aggregated[name] = {"name": name, "value": value, "sum_price": sum_price}


    
    # Преобразуем словарь обратно в список
    result = list(aggregated.values())
    return result
    
   
        

@router.get("/stats/listsell_positions_7d", tags=["Stats"])
def get_lists_positions_7d(db: Session = Depends(get_db)):
    res_positions = db.execute(
        select(Product.name, func.sum(OrderItem.qty), func.sum(OrderItem.price_retail * OrderItem.qty))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.qty).desc())
        .where(OrderItem.created_at >= today_start - timedelta(days=7))
    ).all()
    return [{"name": row[0], "value": row[1], "sum_price": round(row[2], 2)} for row in res_positions]

@router.get("/stats/listsell_positions_30d", tags=["Stats"])
def get_lists_positions_30d(db: Session = Depends(get_db)):
    res_positions = db.execute(
        select(Product.name, func.sum(OrderItem.qty), func.sum(OrderItem.price_retail * OrderItem.qty))
        .join(OrderItem)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.qty).desc())
        .where(OrderItem.created_at >= today_start - timedelta(days=30))
    ).all()
    return [{"name": row[0], "value": row[1], "sum_price": round(row[2], 2)} for row in res_positions]
    
@router.get("/stats/income_by_payment_type_today", tags=["Stats"])
def get_income_by_payment_type_today(db: Session = Depends(get_db)):
    results = db.execute(
        select(
            Order.payment_type, 
            func.sum(Order.sum_order).label('total')
        )
        .where(
            and_(
                Order.created_at >= today_start,
                Order.status == OrderStatus.ending
            )
        )
        .group_by(Order.payment_type)
    ).all()
    
    income_by_type = {row[0]: float(row[1]) for row in results}
    
    return {"cash": income_by_type.get('cash', 0.0), "card": income_by_type.get('card', 0.0)}


@router.get("/stats/income_by_payment_type_7d", tags=["Stats"])
def get_income_by_payment_type_7d(db: Session = Depends(get_db)):
    results = db.execute(
        select(
            Order.payment_type, 
            func.sum(Order.sum_order).label('total')
        )
        .where(
            and_(
                Order.created_at >= today_start - timedelta(days=7),
                Order.status == OrderStatus.ending
            )
        )
        .group_by(Order.payment_type)
    ).all() 
    income_by_type = {row[0]: float(row[1]) for row in results}
    return {
        
            "cash": income_by_type.get('cash', 0.0),
            "card": income_by_type.get('card', 0.0)
       
    }
@router.get("/stats/income_by_payment_type_30d", tags=["Stats"])
def get_income_by_payment_type_30d(db: Session = Depends(get_db)):
    results = db.execute(
        select(
            Order.payment_type, 
            func.sum(Order.sum_order).label('total')
        )
        .where(
            and_(
                Order.created_at >= today_start - timedelta(days=30),
                Order.status == OrderStatus.ending
            )
        )
        .group_by(Order.payment_type)
    ).all()
    income_by_type = {row[0]: float(row[1]) for row in results}
    return {
        
        "cash": income_by_type.get('cash', 0.0),
        "card": income_by_type.get('card', 0.0)
    }