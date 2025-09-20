#!/usr/bin/env python3
"""
Simple script to clear existing PDFs from database using direct Supabase connection
"""

import os
import asyncio
from supabase import create_client, Client

# Supabase configuration (you'll need to add your actual values)
SUPABASE_URL = "your-supabase-url"  # Replace with your actual Supabase URL
SUPABASE_KEY = "your-supabase-anon-key"  # Replace with your actual Supabase anon key

async def clear_database():
    """Clear all existing PDFs from database"""
    try:
        # Create Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Delete all existing PDFs
        result = supabase.table('pdf_documents').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print(f"🗑️  Cleared {len(result.data)} PDFs from database")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning database: {e}")
        print("   Please check your Supabase URL and key in the script")
        return False

async def main():
    print("🗑️  Clearing existing PDFs from database...")
    print("⚠️  Note: You need to update SUPABASE_URL and SUPABASE_KEY in this script first")
    
    # Check if credentials are set
    if SUPABASE_URL == "your-supabase-url" or SUPABASE_KEY == "your-supabase-anon-key":
        print("❌ Please update the Supabase credentials in the script first")
        print("   Edit simple_clear_database.py and replace:")
        print("   - SUPABASE_URL with your actual Supabase URL")
        print("   - SUPABASE_KEY with your actual Supabase anon key")
        return
    
    success = await clear_database()
    
    if success:
        print("✅ Database cleared successfully!")
        print("   Ready for fresh PDF uploads with clean text extraction.")
    else:
        print("❌ Failed to clear database")

if __name__ == "__main__":
    asyncio.run(main())
