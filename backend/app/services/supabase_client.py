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
            print(f"🔍 Supabase: Getting conversations for user_id: {user_id}")
            
            # Use direct table query with service role (bypasses RLS)
            response = self.client.table("conversations").select("*").eq("user_id", user_id).order("updated_at", desc=True).execute()
            
            print(f"📊 Supabase: Raw response data: {response.data}")
            print(f"📊 Supabase: Response count: {len(response.data) if response.data else 0}")
            
            if response.data:
                print(f"✅ Supabase: Retrieved {len(response.data)} conversations for user {user_id}:")
                for i, conv in enumerate(response.data):
                    print(f"   {i+1}. ID: {conv.get('id')}, Title: {conv.get('title')}, Updated: {conv.get('updated_at')}")
            else:
                print(f"❌ Supabase: No conversations found for user {user_id}")
                
            return response.data if response.data else []
        except Exception as e:
            print(f"❌ Supabase: Error getting user conversations: {e}")
            print(f"❌ Supabase: Error type: {type(e)}")
            import traceback
            print(f"❌ Supabase: Traceback: {traceback.format_exc()}")
            return []
    
    async def create_conversation(self, user_id: str, title: str) -> Optional[Dict[str, Any]]:
        """Create new conversation"""
        try:
            # First, ensure the user profile exists
            await self.ensure_user_profile_exists(user_id)
            
            conversation_data = {
                "user_id": user_id,
                "title": title
            }
            print(f"Creating conversation with data: {conversation_data}")
            # Use service role to bypass RLS
            response = self.client.table("conversations").insert(conversation_data).execute()
            print(f"Conversation created, response: {response.data}")
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating conversation: {e}")
            return None
    
    async def ensure_user_profile_exists(self, user_id: str) -> None:
        """Ensure user profile exists, create if it doesn't"""
        try:
            # Check if profile exists
            response = self.client.table("profiles").select("*").eq("id", user_id).execute()
            
            if not response.data:
                print(f"📝 Creating profile for user: {user_id}")
                
                # Try to get user info from auth.users table first
                try:
                    auth_response = self.client.auth.admin.get_user_by_id(user_id)
                    if auth_response.user:
                        user_email = auth_response.user.email or f"user-{user_id[:8]}@example.com"
                        user_name = auth_response.user.user_metadata.get('full_name', 'User')
                        print(f"📧 Found auth user: {user_email}, name: {user_name}")
                    else:
                        user_email = f"user-{user_id[:8]}@example.com"
                        user_name = "User"
                except Exception as auth_error:
                    print(f"⚠️ Could not get auth user info: {auth_error}")
                    user_email = f"user-{user_id[:8]}@example.com"
                    user_name = "User"
                
                profile_data = {
                    "id": user_id,
                    "full_name": user_name,
                    "email": user_email,
                    "phone_number": "+1234567890",
                    "address": "Address not provided"
                }
                
                result = self.client.table("profiles").insert(profile_data).execute()
                if result.data:
                    print(f"✅ Profile created successfully: {result.data[0]}")
                else:
                    print(f"❌ Failed to create profile: {result}")
            else:
                print(f"✅ Profile already exists for user: {user_id}")
                
        except Exception as e:
            print(f"❌ Error ensuring profile exists: {e}")
            import traceback
            print(f"❌ Traceback: {traceback.format_exc()}")
    
    async def get_conversation_messages(self, conversation_id: str, user_id: str) -> List[Dict[str, Any]]:
        """Get conversation messages"""
        try:
            print(f"🔍 Supabase: Getting messages for conversation {conversation_id}, user {user_id}")
            
            # First verify the conversation belongs to the user
            conv_response = self.client.table("conversations").select("id").eq("id", conversation_id).eq("user_id", user_id).execute()
            if not conv_response.data:
                print(f"Conversation {conversation_id} not found or doesn't belong to user {user_id}")
                return []
            
            # Get messages for the conversation
            response = self.client.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at", desc=False).execute()
            print(f"📊 Supabase: Messages response data: {response.data}")
            print(f"📊 Supabase: Messages count: {len(response.data) if response.data else 0}")
            
            return response.data if response.data else []
        except Exception as e:
            print(f"❌ Supabase: Error getting conversation messages: {e}")
            print(f"❌ Supabase: Error type: {type(e)}")
            import traceback
            print(f"❌ Supabase: Traceback: {traceback.format_exc()}")
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
            print(f"Inserting message data: {message_data}")
            # Use service role to bypass RLS
            response = self.client.table("messages").insert(message_data).execute()
            print(f"Message insert response: {response}")
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
    
    async def search_pdf_documents(self, query_embedding: List[float], threshold: float = None, limit: int = None) -> List[Dict[str, Any]]:
        """Search PDF documents using vector similarity"""
        try:
            response = self.client.rpc("search_pdf_documents", {
                "query_embedding": query_embedding,
                "match_threshold": threshold or settings.RAG_SIMILARITY_THRESHOLD,
                "match_count": limit or settings.RAG_MAX_RESULTS
            }).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error searching PDF documents: {e}")
            return []
    
    async def search_pdf_documents_by_category(self, category: str, department: str = None) -> List[Dict[str, Any]]:
        """Search PDF documents by RTI category"""
        try:
            response = self.client.rpc("search_pdf_documents_by_category", {
                "category": category,
                "department": department
            }).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error searching PDF documents by category: {e}")
            return []
    
    async def add_pdf_document(self, title: str, description: str, file_name: str, file_data: bytes, 
                              file_size: int, extracted_text: str, embedding: List[float], 
                              rti_category: str, rti_department: str = None, metadata: Dict = None) -> Dict[str, Any]:
        """Add a PDF document to the knowledge base"""
        try:
            # Convert bytes to base64 for Supabase storage
            import base64
            file_data_base64 = base64.b64encode(file_data).decode('utf-8')
            
            print(f"Original file_data type: {type(file_data)}")
            print(f"Base64 file_data type: {type(file_data_base64)}")
            print(f"Base64 length: {len(file_data_base64)}")
            
            response = self.client.table("pdf_documents").insert({
                "title": title,
                "description": description,
                "file_name": file_name,
                "file_data": file_data_base64,  # Store as base64 string
                "file_size": file_size,
                "file_type": "application/pdf",
                "extracted_text": extracted_text,
                "embedding": embedding,
                "rti_category": rti_category,
                "rti_department": rti_department,
                "metadata": metadata or {}
            }).execute()
            
            print(f"Successfully added PDF document: {title}")
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding PDF document: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_pdf_document(self, document_id: str) -> Dict[str, Any]:
        """Get a PDF document by ID"""
        try:
            response = self.client.table("pdf_documents").select("*").eq("id", document_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting PDF document: {e}")
            return None

# Global service instance
supabase_service = SupabaseService()

def get_supabase_client() -> SupabaseService:
    """Get Supabase service instance"""
    return supabase_service
