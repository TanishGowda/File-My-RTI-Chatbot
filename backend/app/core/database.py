"""
Database configuration and connection management
"""

import asyncio
from supabase import create_client, Client
from app.core.config import settings

# Global Supabase client
supabase: Client = None

def init_db():
    """Initialize database connection"""
    global supabase
    
    try:
        # Use service role key for admin operations
        supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
        print("✅ Supabase client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Supabase client: {e}")
        raise

def get_supabase() -> Client:
    """Get Supabase client instance"""
    if supabase is None:
        init_db()  # Initialize if not already done
    return supabase

def get_supabase_client() -> Client:
    """Get Supabase client instance (alias for compatibility)"""
    return get_supabase()
