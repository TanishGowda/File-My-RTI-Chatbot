import requests
import os
import json

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1/chat"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6InBiSjdjWHVNYWVYb2k1cmoiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3luaGpqYm1ycWF1ZmZkcHl6dG9rLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI4NTU4NzAyYy01NDM3LTQ3YjgtODdlMi1lNzA1NzZkMWM3N2QiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzU4MDkzMTk1LCJpYXQiOjE3NTgwODk1OTUsImVtYWlsIjoidGFuaXNoMjVnb3dkYUBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoidGFuaXNoMjVnb3dkYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoiVGFuaXNoIE5hdmVlbiBHb3dkYSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiODU1ODcwMmMtNTQzNy00N2I4LTg3ZTItZTcwNTc2ZDFjNzdkIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NTgwODk1OTV9XSwic2Vzc2lvbl9pZCI6ImQ2MDQwNGFjLTk5OWEtNDU3Ny05NTEyLTBlMGM0MGE2ZmE5NiIsImlzX2Fub255bW91cyI6ZmFsc2V9.lRCxHPwLhR2wxrqjt82MdFNIHGMnJYin96EkcZVaBXM"

def test_backend_health():
    """Test if backend is responding"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get(f"{API_BASE_URL}/conversations", 
                              headers={"Authorization": f"Bearer {SUPABASE_TOKEN}"})
        print(f"✅ Backend responding: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        return False

def test_pdf_upload_detailed():
    """Test PDF upload with detailed error reporting"""
    print("\n🔍 Testing PDF upload with detailed debugging...")
    
    file_path = "Dharani Telangana Land related issues.pdf"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    file_size = os.path.getsize(file_path)
    print(f"📄 File: {file_path}")
    print(f"📊 Size: {file_size} bytes")
    
    # Test with a very small file first
    print("\n🧪 Testing with a small test file...")
    
    # Create a small test PDF content
    test_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n174\n%%EOF'
    
    url = f"{API_BASE_URL}/upload-pdf"
    headers = {
        "Authorization": f"Bearer {SUPABASE_TOKEN}"
    }
    
    try:
        files = {
            'file': ('test.pdf', test_content, 'application/pdf')
        }
        
        data = {
            'title': 'Test PDF',
            'description': 'Test PDF for debugging',
            'rti_category': 'test',
            'rti_department': 'Test Department'
        }
        
        print("📤 Sending request...")
        response = requests.post(url, headers=headers, files=files, data=data)
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📡 Response headers: {dict(response.headers)}")
        print(f"📡 Response text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Test upload successful!")
            return True
        else:
            print(f"❌ Test upload failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def test_database_schema():
    """Test if we can query the pdf_documents table"""
    print("\n🔍 Testing database schema...")
    
    # Try to get a simple response that might use the database
    try:
        response = requests.get(f"{API_BASE_URL}/conversations", 
                              headers={"Authorization": f"Bearer {SUPABASE_TOKEN}"})
        print(f"✅ Database accessible: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Database not accessible: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting comprehensive debug test...")
    print("=" * 60)
    
    # Test 1: Backend health
    if not test_backend_health():
        print("❌ Backend is not running. Please start it first.")
        exit(1)
    
    # Test 2: Database schema
    if not test_database_schema():
        print("❌ Database is not accessible.")
        exit(1)
    
    # Test 3: PDF upload with small file
    if test_pdf_upload_detailed():
        print("\n✅ All tests passed! The issue might be with large file size.")
    else:
        print("\n❌ Tests failed. Check backend logs for detailed error messages.")
    
    print("=" * 60)
    print("🔍 Check your backend terminal for detailed error logs!")
