
from .health import router as health_router
from .client import router as client_router
from .product import router as product_router
from .order import router as order_router
from fastapi import APIRouter
from .stats import router as stats_router
from .print import router as print_router
router = APIRouter()


router = APIRouter(prefix="/api")
router.include_router(health_router)
router.include_router(client_router)
router.include_router(product_router)
router.include_router(order_router)
router.include_router(stats_router)
router.include_router(print_router)