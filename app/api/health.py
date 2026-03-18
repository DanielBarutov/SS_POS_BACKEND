
from fastapi import APIRouter


router = APIRouter()


@router.get("/version", tags=["DEV"])
async def check_version():
    return f"""ALL IS FINE!
            VERSION - 00"""


@router.get("/health", tags=["DEV"])
async def check_health():
    return f"""ALL IS FINE!
            PROJECT - SUSHISAN"""
