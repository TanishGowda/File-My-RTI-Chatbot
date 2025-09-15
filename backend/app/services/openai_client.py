"""
OpenAI client service for AI operations
"""

import openai
from typing import List, Dict, Any, Optional
from app.core.config import settings
import tiktoken
import json

class OpenAIService:
    """Service class for OpenAI operations"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text"""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []
    
    def get_chat_completion(self, messages: List[Dict[str, str]], context: str = None) -> str:
        """Get chat completion from OpenAI"""
        try:
            # Prepare system message with RTI context
            system_message = self._get_system_message(context)
            
            # Add system message to the beginning
            full_messages = [{"role": "system", "content": system_message}] + messages
            
            print(f"OpenAI request - System message: {system_message[:100]}...")
            print(f"OpenAI request - User messages: {messages}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            print(f"OpenAI response: {result[:100]}...")
            return result
        except Exception as e:
            print(f"Error getting chat completion: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."
    
    def _get_system_message(self, context: str = None) -> str:
        """Get system message for RTI chatbot"""
        base_system_message = """You are FileMyRTI AI, an expert assistant for Right to Information (RTI) applications in India.

CRITICAL INSTRUCTIONS:
- ALWAYS answer the user's question directly and specifically
- NEVER give generic responses like "How can I help you with your RTI application today?"
- If asked "What is RTI?", explain what RTI is clearly and concisely
- If asked to draft an RTI application, provide a complete template
- Be helpful, specific, and direct

EXAMPLES OF GOOD RESPONSES:
User: "What is RTI?"
You: "RTI (Right to Information) is a fundamental right under Article 19(1) of the Indian Constitution. It allows citizens to request information from any public authority. The RTI Act 2005 enables you to ask questions, seek information, take copies of documents, and inspect government work..."

User: "Draft an RTI for passport delay"
You: "Here's a complete RTI application for passport delay:

To: The Central Public Information Officer
Ministry of External Affairs
New Delhi

Subject: Request for Information regarding Passport Application Status

Sir/Madam,

Under Section 6(1) of the Right to Information Act, 2005, I request the following information regarding my passport application:

1. Current status of my passport application (File No: [Your File Number])
2. Reasons for delay in processing
3. Expected date of completion
4. Name and designation of the officer handling my case
5. Any documents required from my side

I am ready to pay the prescribed fee for this information.

Yours faithfully,
[Your Name]
[Your Address]
[Date]"

You are knowledgeable about:
- RTI Act 2005 and its procedures
- RTI application formats and requirements
- Government departments and their RTI procedures
- Fees, exemptions, and appeal processes

Always provide specific, actionable responses that directly answer the user's question."""

        if context:
            base_system_message += f"\n\nRelevant Context:\n{context}"
        
        return base_system_message
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def is_rti_related(self, message: str) -> bool:
        """Check if message is RTI-related"""
        rti_keywords = [
            "rti", "right to information", "information act", "public information",
            "government information", "transparency", "pio", "public authority",
            "information officer", "appeal", "first appeal", "second appeal",
            "information commission", "rti application", "rti query"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in rti_keywords)
    
    def extract_rti_requirements(self, message: str) -> Dict[str, Any]:
        """Extract RTI requirements from user message"""
        try:
            prompt = f"""
            Analyze this RTI request and extract key information:
            
            User Message: "{message}"
            
            Extract and return as JSON:
            {{
                "department": "suggested department or public authority",
                "subject": "suggested subject line",
                "information_request": "specific information being requested",
                "is_valid_rti": true/false,
                "suggestions": "any suggestions for improvement"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            # Try to parse JSON response
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return {
                    "department": "General",
                    "subject": "RTI Application",
                    "information_request": message,
                    "is_valid_rti": True,
                    "suggestions": "Please provide more specific details about the information you need."
                }
        except Exception as e:
            print(f"Error extracting RTI requirements: {e}")
            return {
                "department": "General",
                "subject": "RTI Application",
                "information_request": message,
                "is_valid_rti": True,
                "suggestions": "Please provide more specific details about the information you need."
            }

# Global service instance
openai_service = OpenAIService()

def get_openai_client() -> OpenAIService:
    """Get OpenAI service instance"""
    return openai_service
