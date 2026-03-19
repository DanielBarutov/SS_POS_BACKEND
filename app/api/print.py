from fastapi import APIRouter, HTTPException
from app.driver.pre_check import print_receipt_pred
from app.api.order import OrderItemCreate
from app.driver.cook_check import print_receipt_cook
from app.driver.stats_data_check import print_stats_data_check
from app.driver.stats_position_check import print_stats_positions_check
from pydantic import BaseModel

class ItemStatsPositions(BaseModel):
    name: str
    sum_price: float
    value: int

router = APIRouter()

@router.post("/print/receipt") #Берем selectedOrder и печатаем его
def print_receipt(items: list[OrderItemCreate], sum_order: float, phone: str, order_id: int, address: str | None = None, devices: int | None = None, comment: str | None = None, payment_type: str | None = None):
    try:
        print_receipt_pred(items, sum_order, phone, order_id, address, devices, comment, payment_type)
        return {"status": "success", "message": "Печать выполнена"}
    except Exception as e:
        return {
        "status": "error",
        "message": f"Ошибка принтера: {str(e)}",
        "error_code": "PRINTER_ERROR"
        }

@router.post("/print/cook_check")
def print_cook_check(items: list[OrderItemCreate], order_id: int, devices: int, comment: str):
    try: 
        print_receipt_cook(items, order_id, devices, comment)
        return {"status": "success", "message": "Печать выполнена"}
    except Exception as e:
        return {
        "status": "error",
        "message": f"Ошибка принтера: {str(e)}",
        "error_code": "PRINTER_ERROR"
        }

@router.post("/print/stats_data")
def print_stats_data(income_cash: float|None = None, income_card: float|None = None, total_orders: int|None = None, income_total: float|None = None, income_average: float|None = None):
    try:
        print_stats_data_check(income_cash, income_card, total_orders, income_total, income_average)
        return {"status": "success", "message": "Печать выполнена"}

    except PermissionError as e:
        return {
        "status": "warning",
        "message": f"Ошибка прав доступа: {str(e)}. Проверьте sudo chmod 666 /dev/usb/lp3",
        "error_code": "PERMISSION_DENIED"
        }
        
    except Exception as e:
        return {
        "status": "error",
        "message": f"Ошибка принтера: {str(e)}",
        "error_code": "PRINTER_ERROR"
        }
    

@router.post("/print/stats_positions")
def print_stats_positions(products: list[ItemStatsPositions]):
    try:
        print_stats_positions_check(products)
        return {"status": "success", "message": "Печать выполнена"}
    except Exception as e:
        return {
        "status": "error",
        "message": f"Ошибка принтера: {str(e)}",
        "error_code": "PRINTER_ERROR"
        }