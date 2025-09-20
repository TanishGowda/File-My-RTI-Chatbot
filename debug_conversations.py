#!/usr/bin/env python3
"""
Debug script to check what conversations are in the database
"""

import os
import sys
sys.path.append('backend')

from backend.app.core.database import get_supabase

def debug_conversations():
    try:
        print("🔍 Debugging conversations in database...")
        
        # Initialize Supabase client
        supabase = get_supabase()
        print("✅ Supabase client initialized")
        
        # Get all conversations
        response = supabase.client.table("conversations").select("*").execute()
        conversations = response.data
        
        print(f"📊 Found {len(conversations)} conversations in database:")
        print("=" * 80)
        
        for i, conv in enumerate(conversations, 1):
            print(f"{i}. ID: {conv.get('id')}")
            print(f"   Title: '{conv.get('title')}'")
            print(f"   User ID: {conv.get('user_id')}")
            print(f"   Created: {conv.get('created_at')}")
            print(f"   Updated: {conv.get('updated_at')}")
            print("-" * 40)
        
        # Get all messages
        response = supabase.client.table("messages").select("*").execute()
        messages = response.data
        
        print(f"📝 Found {len(messages)} messages in database:")
        print("=" * 80)
        
        for i, msg in enumerate(messages, 1):
            print(f"{i}. ID: {msg.get('id')}")
            print(f"   Conversation ID: {msg.get('conversation_id')}")
            print(f"   Sender: {msg.get('sender')}")
            print(f"   Content: '{msg.get('content', '')[:100]}...'")
            print(f"   Created: {msg.get('created_at')}")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_conversations()
