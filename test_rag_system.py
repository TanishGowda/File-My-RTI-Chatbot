#!/usr/bin/env python3
"""
Test RAG system functionality
"""

import requests
import json

def test_rag_system():
    print("🔍 Testing RAG System...")
    
    # Test 1: Send a chat message to see if RAG is working
    url = 'http://localhost:8000/api/v1/chat/send'
    headers = {
        'Authorization': 'Bearer test-token'
    }
    
    data = {
        'message': 'How do I file an RTI for land records?',
        'conversation_id': 'test-conversation',
        'user_id': '550e8400-e29b-41d4-a716-446655440000'
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"Chat Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ RAG system is working!")
            print(f"Full response: {result}")
            
            # Check different possible response structures
            message = None
            if "data" in result and "message" in result["data"]:
                message = result["data"]["message"]
            elif "message" in result:
                message = result["message"]
            elif "response" in result:
                message = result["response"]
            
            if message:
                print(f"Response: {message[:200]}...")
                
                # Check if response mentions RTI formats or templates
                if any(keyword in message.lower() for keyword in ['rti', 'format', 'template', 'application', 'land', 'records']):
                    print("✅ Response contains RTI-related content!")
                else:
                    print("⚠️ Response may not be using RAG context")
            else:
                print("⚠️ Could not extract message from response")
        else:
            print(f"❌ Chat failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    
    # Test 2: Test RTI draft generation
    print("🔍 Testing RTI Draft Generation...")
    
    draft_url = 'http://localhost:8000/api/v1/chat/generate-rti-draft'
    draft_data = {
        'message': 'I need to file an RTI for land mutation records in Telangana',
        'user_id': '550e8400-e29b-41d4-a716-446655440000'
    }
    
    try:
        response = requests.post(draft_url, headers=headers, json=draft_data)
        print(f"Draft Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ RTI draft generation is working!")
            draft = result.get("data", {}).get("draft_content", "No draft")
            print(f"Draft: {draft[:200]}...")
        else:
            print(f"❌ Draft generation failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_rag_system()
