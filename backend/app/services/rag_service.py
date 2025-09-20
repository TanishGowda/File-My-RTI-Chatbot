"""
RAG (Retrieval-Augmented Generation) service for enhanced AI responses using PDF documents
"""

from typing import List, Dict, Any, Optional
from app.services.openai_client import get_openai_client
from app.services.supabase_client import get_supabase_client
from app.core.config import settings

class RAGService:
    """Service class for RAG operations with PDF documents"""
    
    def __init__(self):
        self.openai_client = get_openai_client()
        self.supabase_client = get_supabase_client()
    
    async def get_relevant_context(self, query: str) -> str:
        """Get relevant context for a query using vector similarity search on PDF documents"""
        try:
            print(f"RAG Query: {query}")
            
            # Generate embedding for the query
            query_embedding = await self._generate_embedding(query)
            print(f"Query embedding generated: {len(query_embedding)} dimensions")
            
            # Search PDF documents using vector similarity
            results = await self.supabase_client.search_pdf_documents(
                query_embedding=query_embedding,
                threshold=settings.RAG_SIMILARITY_THRESHOLD,
                limit=settings.RAG_MAX_RESULTS
            )
            
            print(f"Found {len(results)} relevant documents")
            
            # Format context from results with better prioritization
            context_parts = []
            for i, result in enumerate(results):
                similarity = result.get('similarity', 0)
                print(f"Document {i+1}: {result['title']} (similarity: {similarity:.3f})")
                
                context_parts.append(f"=== RTI TEMPLATE {i+1} ===")
                context_parts.append(f"Title: {result['title']}")
                context_parts.append(f"Category: {result['rti_category']}")
                if result.get('rti_department'):
                    context_parts.append(f"Department: {result['rti_department']}")
                context_parts.append(f"Similarity Score: {similarity:.3f}")
                context_parts.append(f"EXACT FORMAT:")
                context_parts.append(result['extracted_text'])  # Use full text for exact templates
                context_parts.append("=" * 50)
            
            context = "\n".join(context_parts)
            print(f"Context length: {len(context)} characters")
            return context
        
        except Exception as e:
            print(f"Error getting relevant context: {e}")
            return ""
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        try:
            response = self.openai_client.client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    async def generate_rti_draft(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate RTI draft using PDF-based RAG"""
        try:
            # Get relevant PDF context
            context = await self.get_relevant_context(user_message)
            
            # Extract RTI requirements
            rti_requirements = self.openai_client.extract_rti_requirements(user_message)
            
            # Generate RTI draft using the PDF format as template
            draft_prompt = f"""
            Based on the user's request and the relevant RTI format templates from PDF documents, generate a complete RTI application draft.
            
            User Request: {user_message}
            Extracted Requirements: {rti_requirements}
            
            Available RTI Format Templates:
            {context}
            
            Instructions:
            1. Use the most relevant RTI format template from the PDF documents above
            2. Adapt the template to match the user's specific request
            3. Fill in the placeholders with appropriate information
            4. Maintain the exact format and structure from the template
            5. Ensure all legal requirements are met
            
            Generate a complete RTI application following the template format:
            """
            
            response = self.openai_client.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": draft_prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            draft_content = response.choices[0].message.content
            
            return {
                "draft_content": draft_content,
                "department": rti_requirements.get("department", "General"),
                "subject": rti_requirements.get("subject", "RTI Application"),
                "is_valid_rti": rti_requirements.get("is_valid_rti", True),
                "suggestions": rti_requirements.get("suggestions", ""),
                "context_used": context,
                "format_source": "PDF Template"
            }
        
        except Exception as e:
            print(f"Error generating RTI draft: {e}")
            return {
                "draft_content": "I apologize, but I'm having trouble generating the RTI draft right now. Please try again later.",
                "department": "General",
                "subject": "RTI Application",
                "is_valid_rti": True,
                "suggestions": "Please try rephrasing your request with more specific details.",
                "context_used": "",
                "format_source": "Default"
            }
    
    async def get_enhanced_response(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Get enhanced AI response using PDF-based RAG"""
        try:
            # Get relevant PDF context
            context = await self.get_relevant_context(user_message)
            
            # Prepare conversation messages with context
            messages = conversation_history or []
            
            # Add system message with RTI context
            system_message = {
                "role": "system",
                "content": f"""You are an expert RTI (Right to Information) assistant. You help users with RTI applications, provide information about the RTI Act 2005, and assist with drafting RTI applications.

CRITICAL INSTRUCTIONS:
1. ALWAYS use the EXACT format from the PDF templates provided below
2. Copy the exact addresses, department names, and structure from the templates
3. Do NOT modify or generalize the template format
4. Use the specific details from the most relevant template

Available RTI Format Templates and Information:
{context}

When users ask about RTI applications, you MUST use the exact format from the PDF templates above. Copy the exact addresses, department names, and structure. Do not create generic formats."""
            }
            
            messages.insert(0, system_message)
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
