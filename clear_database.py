#!/usr/bin/env python3
"""
Script to clear existing PDFs from database
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.append('backend')

# Change to backend directory for imports
os.chdir('backend')
from app.services.supabase_client import get_supabase_client

async def clear_database():
    """Clear all existing PDFs from database"""
    try:
        supabase = get_supabase_client()
        
        # Delete all existing PDFs
        result = supabase.client.table('pdf_documents').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print(f"🗑️  Cleared {len(result.data)} PDFs from database")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning database: {e}")
        return False

async def main():
    print("🗑️  Clearing existing PDFs from database...")
    
    success = await clear_database()
    
    if success:
        print("✅ Database cleared successfully!")
        print("   Ready for fresh PDF uploads with clean text extraction.")
    else:
        print("❌ Failed to clear database")

if __name__ == "__main__":
    asyncio.run(main())
