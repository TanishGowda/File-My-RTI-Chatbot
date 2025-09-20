"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, chat, rti, profiles, rti_applications

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(rti.router, prefix="/rti", tags=["rti"])
api_router.include_router(rti_applications.router, prefix="/rti-applications", tags=["rti-applications"])
