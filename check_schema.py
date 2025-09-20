#!/usr/bin/env python3
"""
Check the database schema for pdf_documents table
"""

import requests
import json

def check_schema():
    print("🔍 Checking database schema...")
    
    # Your Supabase URL and anon key
    SUPABASE_URL = "https://your-project.supabase.co"  # Replace with your actual URL
    SUPABASE_ANON_KEY = "your-anon-key"  # Replace with your actual key
    
    # Test endpoint
    url = "http://localhost:8000/api/v1/chat/upload-pdf"
    
    # Test with minimal data
    test_data = {
        "title": "Test Document",
        "description": "Test Description", 
        "rti_category": "test",
        "rti_department": "test"
    }
    
    # Create a small test PDF content (just a few bytes)
    test_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
    
    files = {
        'file': ('test.pdf', test_pdf_content, 'application/pdf')
    }
    
    headers = {
        'Authorization': 'Bearer test-token'
    }
    
    try:
        response = requests.post(url, data=test_data, files=files, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Schema is correct - upload should work!")
        else:
            print("❌ Schema issue - check the error message")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_schema()
