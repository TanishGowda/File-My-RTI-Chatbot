"""
RAG (Retrieval-Augmented Generation) service for enhanced AI responses
"""

from typing import List, Dict, Any, Optional
from app.services.openai_client import get_openai_client
from app.services.supabase_client import get_supabase_client
from app.core.config import settings

class RAGService:
    """Service class for RAG operations"""
    
    def __init__(self):
        self.openai_client = get_openai_client()
        self.supabase_client = get_supabase_client()
    
    async def get_relevant_context(self, query: str) -> str:
        """Get relevant context for a query using RAG"""
        try:
            # Search knowledge base using text similarity
            results = await self.supabase_client.search_knowledge_base(
                query_text=query,
                threshold=settings.RAG_SIMILARITY_THRESHOLD,
                limit=settings.RAG_MAX_RESULTS
            )
            
            # Format context from results
            context_parts = []
            for result in results:
                context_parts.append(f"Title: {result['title']}\nContent: {result['content']}")
                if result.get('source_url'):
                    context_parts.append(f"Source: {result['source_url']}")
                context_parts.append("---")
            
            return "\n".join(context_parts)
        
        except Exception as e:
            print(f"Error getting relevant context: {e}")
            return ""
    
    async def generate_rti_draft(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate RTI draft using RAG"""
        try:
            # Get relevant context
            context = await self.get_relevant_context(user_message)
            
            # Extract RTI requirements
            rti_requirements = self.openai_client.extract_rti_requirements(user_message)
            
            # Generate RTI draft
            draft_prompt = f"""
            Based on the user's request and the relevant context, generate a complete RTI application draft.
            
            User Request: {user_message}
            Extracted Requirements: {rti_requirements}
            
            Context:
            {context}
            
            Generate a complete RTI application in the following format:
            
            Subject: [Clear, specific subject line]
            
            To,
            [Appropriate Public Information Officer]
            [Department/Public Authority Name]
            [Address]
            
            From,
            [User's Name]
            [User's Address]
            
            Date: [Current Date]
            
            Sir/Madam,
            
            Under the Right to Information Act, 2005, I request the following information:
            
            [Specific information request in numbered points]
            
            1. [First information request]
            2. [Second information request]
            [Continue as needed]
            
            I request that the information be provided in [format preference - digital/physical].
            
            If any part of the information is exempted under the RTI Act, please provide the remaining information and cite the relevant exemption clause.
            
            I am ready to pay the prescribed fee for this application.
            
            Thank you for your time and consideration.
            
            Yours faithfully,
            [User's Name]
            [Contact Information]
            
            Enclosures: [if any]
            """
            
            response = self.openai_client.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": draft_prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            
            draft_content = response.choices[0].message.content
            
            return {
                "draft_content": draft_content,
                "department": rti_requirements.get("department", "General"),
                "subject": rti_requirements.get("subject", "RTI Application"),
                "is_valid_rti": rti_requirements.get("is_valid_rti", True),
                "suggestions": rti_requirements.get("suggestions", ""),
                "context_used": context
            }
        
        except Exception as e:
            print(f"Error generating RTI draft: {e}")
            return {
                "draft_content": "I apologize, but I'm having trouble generating the RTI draft right now. Please try again later.",
                "department": "General",
                "subject": "RTI Application",
                "is_valid_rti": True,
                "suggestions": "Please try rephrasing your request with more specific details.",
                "context_used": ""
            }
    
    async def get_enhanced_response(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Get enhanced AI response using RAG"""
        try:
            # Get relevant context
            context = await self.get_relevant_context(user_message)
            
            # Prepare conversation messages
            messages = conversation_history or []
            messages.append({"role": "user", "content": user_message})
            
            # Generate response with context
            response = self.openai_client.get_chat_completion(messages, context)
            
            return response
        
        except Exception as e:
            print(f"Error getting enhanced response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."

# Global service instance
rag_service = RAGService()

def get_rag_service() -> RAGService:
    """Get RAG service instance"""
    return rag_service
