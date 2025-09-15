"""
Supabase client service for authentication and database operations
"""

from typing import Optional, Dict, Any, List
from supabase import Client
from app.core.database import get_supabase
from app.core.config import settings

class SupabaseService:
    """Service class for Supabase operations"""
    
    def __init__(self):
        self.client = get_supabase()
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by user ID"""
        try:
            response = self.client.table("profiles").select("*").eq("id", user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    async def create_user_profile(self, user_id: str, email: str, full_name: str = None) -> Optional[Dict[str, Any]]:
        """Create user profile"""
        try:
            profile_data = {
                "id": user_id,
                "email": email,
                "full_name": full_name
            }
            response = self.client.table("profiles").insert(profile_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return None
    
    async def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user profile"""
        try:
            response = self.client.table("profiles").update(update_data).eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return None
    
    async def get_user_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user conversations"""
        try:
            # Use direct table query with service role (bypasses RLS)
            response = self.client.table("conversations").select("*").eq("user_id", user_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting user conversations: {e}")
            return []
    
    async def create_conversation(self, user_id: str, title: str) -> Optional[Dict[str, Any]]:
        """Create new conversation"""
        try:
            conversation_data = {
                "user_id": user_id,
                "title": title
            }
            # Use service role to bypass RLS
            response = self.client.table("conversations").insert(conversation_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating conversation: {e}")
            return None
    
    async def get_conversation_messages(self, conversation_id: str, user_id: str) -> List[Dict[str, Any]]:
        """Get conversation messages"""
        try:
            # Use direct table query instead of RPC to avoid RLS issues
            response = self.client.table("messages").select("*").eq("conversation_id", conversation_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting conversation messages: {e}")
            return []
    
    async def add_message(self, conversation_id: str, sender: str, content: str, metadata: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Add message to conversation"""
        try:
            message_data = {
                "conversation_id": conversation_id,
                "sender": sender,
                "content": content,
                "metadata": metadata or {}
            }
            # Use service role to bypass RLS
            response = self.client.table("messages").insert(message_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding message: {e}")
            return None
    
    async def create_rti_draft(self, user_id: str, title: str, content: str, department: str = None, subject: str = None) -> Optional[Dict[str, Any]]:
        """Create RTI draft"""
        try:
            draft_data = {
                "user_id": user_id,
                "title": title,
                "content": content,
                "department": department or settings.RTI_DEFAULT_DEPARTMENT,
                "subject": subject
            }
            response = self.client.table("rti_drafts").insert(draft_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating RTI draft: {e}")
            return None
    
    async def get_user_rti_drafts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user RTI drafts"""
        try:
            response = self.client.table("rti_drafts").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting RTI drafts: {e}")
            return []
    
    async def search_knowledge_base(self, query_text: str, threshold: float = None, limit: int = None) -> List[Dict[str, Any]]:
        """Search knowledge base using text similarity"""
        try:
            response = self.client.rpc("search_knowledge_base", {
                "query_text": query_text,
                "match_threshold": threshold or settings.RAG_SIMILARITY_THRESHOLD,
                "match_count": limit or settings.RAG_MAX_RESULTS
            }).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error searching knowledge base: {e}")
            return []

# Global service instance
supabase_service = SupabaseService()

def get_supabase_client() -> SupabaseService:
    """Get Supabase service instance"""
    return supabase_service
