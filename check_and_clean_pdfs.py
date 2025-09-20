#!/usr/bin/env python3
"""
Script to check existing PDFs in database and clean them up
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.append('.')

from app.services.supabase_client import get_supabase_client

async def check_existing_pdfs():
    """Check what PDFs are currently in the database"""
    try:
        supabase = get_supabase_client()
        result = supabase.client.table('pdf_documents').select('id, title, file_name, rti_category').execute()
        
        print(f"📊 Found {len(result.data)} PDFs in database:")
        print("=" * 60)
        
        for i, pdf in enumerate(result.data, 1):
            print(f"{i:2d}. {pdf['title']}")
            print(f"    File: {pdf['file_name']}")
            print(f"    Category: {pdf['rti_category']}")
            print(f"    ID: {pdf['id']}")
            print()
        
        return result.data
        
    except Exception as e:
        print(f"❌ Error checking PDFs: {e}")
        return []

async def clean_database():
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
    print("🔍 Checking existing PDFs in database...")
    print()
    
    # Check existing PDFs
    existing_pdfs = await check_existing_pdfs()
    
    if existing_pdfs:
        print("⚠️  These PDFs contain corrupted text with weird symbols (Ɵ)")
        print("🔄 We need to re-upload them with clean text extraction")
        print()
        
        response = input("Do you want to clear the database and re-upload PDFs? (y/n): ")
        
        if response.lower() == 'y':
            print("\n🗑️  Clearing database...")
            success = await clean_database()
            
            if success:
                print("✅ Database cleared successfully!")
                print("\n📋 Next steps:")
                print("1. Run the upload script to re-upload PDFs with clean text")
                print("2. The character encoding issues will be fixed")
            else:
                print("❌ Failed to clear database")
        else:
            print("ℹ️  Database not cleared. You can manually delete PDFs if needed.")
    else:
        print("✅ Database is empty. Ready for fresh PDF uploads.")

if __name__ == "__main__":
    asyncio.run(main())
