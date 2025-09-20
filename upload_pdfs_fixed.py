import requests
import os
import mimetypes

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1/chat"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6InBiSjdjWHVNYWVYb2k1cmoiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3luaGpqYm1ycWF1ZmZkcHl6dG9rLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI4NTU4NzAyYy01NDM3LTQ3YjgtODdlMi1lNzA1NzZkMWM3N2QiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzU4MDkzMTk1LCJpYXQiOjE3NTgwODk1OTUsImVtYWlsIjoidGFuaXNoMjVnb3dkYUBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoidGFuaXNoMjVnb3dkYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoiVGFuaXNoIE5hdmVlbiBHb3dkYSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiODU1ODcwMmMtNTQzNy00N2I4LTg3ZTItZTcwNTc2ZDFjNzdkIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NTgwODk1OTV9XSwic2Vzc2lvbl9pZCI6ImQ2MDQwNGFjLTk5OWEtNDU3Ny05NTEyLTBlMGM0MGE2ZmE5NiIsImlzX2Fub255bW91cyI6ZmFsc2V9.lRCxHPwLhR2wxrqjt82MdFNIHGMnJYin96EkcZVaBXM"

# Test with just one file first
test_files = [
    {
        "file_path": "Dharani Telangana Land related issues.pdf",
        "title": "Dharani Telangana Land Related RTI Format",
        "description": "RTI format for land-related issues in Telangana Dharani system",
        "rti_category": "land_records",
        "rti_department": "Telangana Revenue Department"
    }
]

def upload_pdf_fixed(file_info):
    """Upload a single PDF file with better content type handling"""
    url = f"{API_BASE_URL}/upload-pdf"
    headers = {
        "Authorization": f"Bearer {SUPABASE_TOKEN}"
    }
    
    # Check if file exists
    if not os.path.exists(file_info["file_path"]):
        print(f"❌ File not found: {file_info['file_path']}")
        return False
    
    # Check file size
    file_size = os.path.getsize(file_info["file_path"])
    if file_size == 0:
        print(f"❌ File is empty: {file_info['file_path']}")
        return False
    
    # Check if it's actually a PDF
    try:
        with open(file_info["file_path"], 'rb') as f:
            first_bytes = f.read(4)
            if first_bytes != b'%PDF':
                print(f"❌ File is not a valid PDF: {file_info['file_path']}")
                return False
    except Exception as e:
        print(f"❌ Error reading file: {file_info['file_path']} - {e}")
        return False
    
    print(f"📄 Uploading: {file_info['file_path']} ({file_size} bytes)")
    
    # Prepare form data with explicit content type
    try:
        with open(file_info["file_path"], 'rb') as f:
            files = {
                'file': (file_info["file_path"], f, 'application/pdf')
            }
            
            data = {
                'title': file_info["title"],
                'description': file_info["description"],
                'rti_category': file_info["rti_category"],
                'rti_department': file_info["rti_department"]
            }
            
            response = requests.post(url, headers=headers, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Successfully uploaded: {file_info['title']}")
                print(f"   Document ID: {result['data']['document_id']}")
                return True
            else:
                print(f"❌ Failed to upload {file_info['title']}: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error uploading {file_info['title']}: {str(e)}")
        return False

# Test with one file first
print("🧪 Testing with one file first...")
print("=" * 50)

for pdf_info in test_files:
    upload_pdf_fixed(pdf_info)

print("=" * 50)
print("✅ Test completed. If successful, we can upload all files.")
