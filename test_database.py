import requests

# Test if the backend can connect to the database
API_BASE_URL = "http://localhost:8000/api/v1/chat"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6InBiSjdjWHVNYWVYb2k1cmoiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3luaGpqYm1ycWF1ZmZkcHl6dG9rLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI4NTU4NzAyYy01NDM3LTQ3YjgtODdlMi1lNzA1NzZkMWM3N2QiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzU4MDkzMTk1LCJpYXQiOjE3NTgwODk1OTUsImVtYWlsIjoidGFuaXNoMjVnb3dkYUBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoidGFuaXNoMjVnb3dkYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoiVGFuaXNoIE5hdmVlbiBHb3dkYSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiODU1ODcwMmMtNTQzNy00N2I4LTg3ZTItZTcwNTc2ZDFjNzdkIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NTgwODk1OTV9XSwic2Vzc2lvbl9pZCI6ImQ2MDQwNGFjLTk5OWEtNDU3Ny05NTEyLTBlMGM0MGE2ZmE5NiIsImlzX2Fub255bW91cyI6ZmFsc2V9.lRCxHPwLhR2wxrqjt82MdFNIHGMnJYin96EkcZVaBXM"

def test_database_connection():
    """Test if the backend can connect to the database"""
    print("🔍 Testing database connection...")
    
    # Test 1: Check if conversations endpoint works
    try:
        response = requests.get(f"{API_BASE_URL}/conversations", 
                              headers={"Authorization": f"Bearer {SUPABASE_TOKEN}"})
        print(f"📡 Conversations endpoint: {response.status_code}")
        if response.status_code == 200:
            print("✅ Database connection working")
        else:
            print(f"❌ Database connection failed: {response.text}")
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False
    
    # Test 2: Check if we can create a conversation
    try:
        response = requests.post(f"{API_BASE_URL}/conversations", 
                               headers={"Authorization": f"Bearer {SUPABASE_TOKEN}"},
                               json={"title": "Test Conversation"})
        print(f"📡 Create conversation: {response.status_code}")
        if response.status_code == 200:
            print("✅ Can create conversations")
        else:
            print(f"❌ Cannot create conversations: {response.text}")
    except Exception as e:
        print(f"❌ Error creating conversation: {e}")
    
    return True

if __name__ == "__main__":
    test_database_connection()
