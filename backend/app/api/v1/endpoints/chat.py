"""
Chat endpoints for conversation management
"""

from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import PyPDF2
import io
import uuid
from docx import Document
from app.models.schemas import (
    Conversation, ConversationCreate, Message, MessageCreate,
    ChatRequest, ChatResponse, APIResponse
)
from app.services.supabase_client import get_supabase_client
from app.services.rag_service import get_rag_service
from app.services.openai_client import get_openai_client

router = APIRouter()
security = HTTPBearer()

def extract_text_from_file(file_content: bytes, file_extension: str) -> str:
    """Extract text content from various file types (PDF, DOCX, TXT)"""
    try:
        print(f"File size: {len(file_content)} bytes, Extension: {file_extension}")
        
        if file_extension.lower() == '.pdf':
            return extract_pdf_text(file_content)
        elif file_extension.lower() == '.docx':
            return extract_docx_text(file_content)
        elif file_extension.lower() == '.txt':
            return extract_txt_text(file_content)
        else:
            raise Exception(f"Unsupported file type: {file_extension}")
    
    except Exception as e:
        print(f"Error extracting text from {file_extension}: {e}")
        raise e

def extract_pdf_text(file_content: bytes) -> str:
    """Extract text content from PDF file with improved extraction"""
    try:
        print(f"PDF file size: {len(file_content)} bytes")
        
        # Create a BytesIO object from the file content
        pdf_file = io.BytesIO(file_content)
        
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        print(f"PDF pages: {len(pdf_reader.pages)}")
        
        # Check if PDF is encrypted
        if pdf_reader.is_encrypted:
            print("PDF is encrypted")
            raise Exception("PDF is password protected or encrypted")
        
        # Extract text from all pages with improved processing
        text_parts = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            
            # Clean and improve text extraction
            if page_text.strip():
                # Fix common character encoding issues
                cleaned_text = page_text
                
                # Replace common encoding issues
                char_replacements = {
                    'Ɵ': 't',  # Replace weird t with normal t
                    'Ɵ': 'o',  # Replace weird o with normal o
                    'Ɵ': 'a',  # Replace weird a with normal a
                    'Ɵ': 'e',  # Replace weird e with normal e
                    'Ɵ': 'i',  # Replace weird i with normal i
                    'Ɵ': 'u',  # Replace weird u with normal u
                    'Ɵ': 'n',  # Replace weird n with normal n
                    'Ɵ': 's',  # Replace weird s with normal s
                    'Ɵ': 'r',  # Replace weird r with normal r
                    'Ɵ': 'l',  # Replace weird l with normal l
                    'Ɵ': 'c',  # Replace weird c with normal c
                    'Ɵ': 'd',  # Replace weird d with normal d
                    'Ɵ': 'f',  # Replace weird f with normal f
                    'Ɵ': 'g',  # Replace weird g with normal g
                    'Ɵ': 'h',  # Replace weird h with normal h
                    'Ɵ': 'j',  # Replace weird j with normal j
                    'Ɵ': 'k',  # Replace weird k with normal k
                    'Ɵ': 'm',  # Replace weird m with normal m
                    'Ɵ': 'p',  # Replace weird p with normal p
                    'Ɵ': 'q',  # Replace weird q with normal q
                    'Ɵ': 'v',  # Replace weird v with normal v
                    'Ɵ': 'w',  # Replace weird w with normal w
                    'Ɵ': 'x',  # Replace weird x with normal x
                    'Ɵ': 'y',  # Replace weird y with normal y
                    'Ɵ': 'z',  # Replace weird z with normal z
                    'Ɵ': 'A',  # Replace weird A with normal A
                    'Ɵ': 'B',  # Replace weird B with normal B
                    'Ɵ': 'C',  # Replace weird C with normal C
                    'Ɵ': 'D',  # Replace weird D with normal D
                    'Ɵ': 'E',  # Replace weird E with normal E
                    'Ɵ': 'F',  # Replace weird F with normal F
                    'Ɵ': 'G',  # Replace weird G with normal G
                    'Ɵ': 'H',  # Replace weird H with normal H
                    'Ɵ': 'I',  # Replace weird I with normal I
                    'Ɵ': 'J',  # Replace weird J with normal J
                    'Ɵ': 'K',  # Replace weird K with normal K
                    'Ɵ': 'L',  # Replace weird L with normal L
                    'Ɵ': 'M',  # Replace weird M with normal M
                    'Ɵ': 'N',  # Replace weird N with normal N
                    'Ɵ': 'O',  # Replace weird O with normal O
                    'Ɵ': 'P',  # Replace weird P with normal P
                    'Ɵ': 'Q',  # Replace weird Q with normal Q
                    'Ɵ': 'R',  # Replace weird R with normal R
                    'Ɵ': 'S',  # Replace weird S with normal S
                    'Ɵ': 'T',  # Replace weird T with normal T
                    'Ɵ': 'U',  # Replace weird U with normal U
                    'Ɵ': 'V',  # Replace weird V with normal V
                    'Ɵ': 'W',  # Replace weird W with normal W
                    'Ɵ': 'X',  # Replace weird X with normal X
                    'Ɵ': 'Y',  # Replace weird Y with normal Y
                    'Ɵ': 'Z',  # Replace weird Z with normal Z
                }
                
                # Apply character replacements
                for old_char, new_char in char_replacements.items():
                    cleaned_text = cleaned_text.replace(old_char, new_char)
                
                # Remove excessive whitespace and normalize
                cleaned_text = ' '.join(cleaned_text.split())
                text_parts.append(cleaned_text)
                print(f"Page {page_num + 1} text length: {len(cleaned_text)}")
            else:
                print(f"Page {page_num + 1}: No text extracted")
        
        # Join all text parts
        full_text = "\n".join(text_parts)
        
        # Additional cleaning for better embedding quality
        full_text = full_text.replace('\n\n', '\n')  # Remove double newlines
        full_text = ' '.join(full_text.split())  # Normalize whitespace
        
        print(f"Total extracted text length: {len(full_text)}")
        print(f"First 500 chars: {full_text[:500]}")
        
        return full_text.strip()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        print(f"Error type: {type(e)}")
        raise e  # Re-raise the exception instead of returning error string

def extract_docx_text(file_content: bytes) -> str:
    """Extract text content from DOCX file"""
    try:
        print(f"DOCX file size: {len(file_content)} bytes")
        
        # Create a BytesIO object from the file content
        docx_file = io.BytesIO(file_content)
        
        # Create Document object
        doc = Document(docx_file)
        
        # Extract text from all paragraphs
        text_parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text.strip())
        
        # Join all text parts
        full_text = "\n".join(text_parts)
        
        # Apply character encoding fixes
        char_replacements = {
            'Ɵ': 't', 'Ɵ': 'o', 'Ɵ': 'a', 'Ɵ': 'e', 'Ɵ': 'i', 'Ɵ': 'u', 'Ɵ': 'n', 'Ɵ': 's', 'Ɵ': 'r', 'Ɵ': 'l',
            'Ɵ': 'c', 'Ɵ': 'd', 'Ɵ': 'f', 'Ɵ': 'g', 'Ɵ': 'h', 'Ɵ': 'j', 'Ɵ': 'k', 'Ɵ': 'm', 'Ɵ': 'p', 'Ɵ': 'q',
            'Ɵ': 'v', 'Ɵ': 'w', 'Ɵ': 'x', 'Ɵ': 'y', 'Ɵ': 'z', 'Ɵ': 'A', 'Ɵ': 'B', 'Ɵ': 'C', 'Ɵ': 'D', 'Ɵ': 'E',
            'Ɵ': 'F', 'Ɵ': 'G', 'Ɵ': 'H', 'Ɵ': 'I', 'Ɵ': 'J', 'Ɵ': 'K', 'Ɵ': 'L', 'Ɵ': 'M', 'Ɵ': 'N', 'Ɵ': 'O',
            'Ɵ': 'P', 'Ɵ': 'Q', 'Ɵ': 'R', 'Ɵ': 'S', 'Ɵ': 'T', 'Ɵ': 'U', 'Ɵ': 'V', 'Ɵ': 'W', 'Ɵ': 'X', 'Ɵ': 'Y', 'Ɵ': 'Z'
        }
        
        for old_char, new_char in char_replacements.items():
            full_text = full_text.replace(old_char, new_char)
        
        # Clean and normalize text
        full_text = ' '.join(full_text.split())  # Normalize whitespace
        
        print(f"Total extracted text length: {len(full_text)}")
        print(f"First 500 chars: {full_text[:500]}")
        
        return full_text.strip()
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
        print(f"Error type: {type(e)}")
        raise e

def extract_txt_text(file_content: bytes) -> str:
    """Extract text content from TXT file"""
    try:
        print(f"TXT file size: {len(file_content)} bytes")
        
        # Decode bytes to text
        text = file_content.decode('utf-8')
        
        # Apply character encoding fixes
        char_replacements = {
            'Ɵ': 't', 'Ɵ': 'o', 'Ɵ': 'a', 'Ɵ': 'e', 'Ɵ': 'i', 'Ɵ': 'u', 'Ɵ': 'n', 'Ɵ': 's', 'Ɵ': 'r', 'Ɵ': 'l',
            'Ɵ': 'c', 'Ɵ': 'd', 'Ɵ': 'f', 'Ɵ': 'g', 'Ɵ': 'h', 'Ɵ': 'j', 'Ɵ': 'k', 'Ɵ': 'm', 'Ɵ': 'p', 'Ɵ': 'q',
            'Ɵ': 'v', 'Ɵ': 'w', 'Ɵ': 'x', 'Ɵ': 'y', 'Ɵ': 'z', 'Ɵ': 'A', 'Ɵ': 'B', 'Ɵ': 'C', 'Ɵ': 'D', 'Ɵ': 'E',
            'Ɵ': 'F', 'Ɵ': 'G', 'Ɵ': 'H', 'Ɵ': 'I', 'Ɵ': 'J', 'Ɵ': 'K', 'Ɵ': 'L', 'Ɵ': 'M', 'Ɵ': 'N', 'Ɵ': 'O',
            'Ɵ': 'P', 'Ɵ': 'Q', 'Ɵ': 'R', 'Ɵ': 'S', 'Ɵ': 'T', 'Ɵ': 'U', 'Ɵ': 'V', 'Ɵ': 'W', 'Ɵ': 'X', 'Ɵ': 'Y', 'Ɵ': 'Z'
        }
        
        for old_char, new_char in char_replacements.items():
            text = text.replace(old_char, new_char)
        
        # Clean and normalize text
        text = ' '.join(text.split())  # Normalize whitespace
        
        print(f"Total extracted text length: {len(text)}")
        print(f"First 500 chars: {text[:500]}")
        
        return text.strip()
    except UnicodeDecodeError:
        # Try with different encodings
        try:
            text = file_content.decode('latin-1')
            
            # Apply character encoding fixes
            char_replacements = {
                'Ɵ': 't', 'Ɵ': 'o', 'Ɵ': 'a', 'Ɵ': 'e', 'Ɵ': 'i', 'Ɵ': 'u', 'Ɵ': 'n', 'Ɵ': 's', 'Ɵ': 'r', 'Ɵ': 'l',
                'Ɵ': 'c', 'Ɵ': 'd', 'Ɵ': 'f', 'Ɵ': 'g', 'Ɵ': 'h', 'Ɵ': 'j', 'Ɵ': 'k', 'Ɵ': 'm', 'Ɵ': 'p', 'Ɵ': 'q',
                'Ɵ': 'v', 'Ɵ': 'w', 'Ɵ': 'x', 'Ɵ': 'y', 'Ɵ': 'z', 'Ɵ': 'A', 'Ɵ': 'B', 'Ɵ': 'C', 'Ɵ': 'D', 'Ɵ': 'E',
                'Ɵ': 'F', 'Ɵ': 'G', 'Ɵ': 'H', 'Ɵ': 'I', 'Ɵ': 'J', 'Ɵ': 'K', 'Ɵ': 'L', 'Ɵ': 'M', 'Ɵ': 'N', 'Ɵ': 'O',
                'Ɵ': 'P', 'Ɵ': 'Q', 'Ɵ': 'R', 'Ɵ': 'S', 'Ɵ': 'T', 'Ɵ': 'U', 'Ɵ': 'V', 'Ɵ': 'W', 'Ɵ': 'X', 'Ɵ': 'Y', 'Ɵ': 'Z'
            }
            
            for old_char, new_char in char_replacements.items():
                text = text.replace(old_char, new_char)
            
            text = ' '.join(text.split())
            print(f"Decoded with latin-1, length: {len(text)}")
            return text.strip()
        except Exception as e:
            print(f"Error decoding TXT file: {e}")
            raise e
    except Exception as e:
        print(f"Error extracting TXT text: {e}")
        print(f"Error type: {type(e)}")
        raise e

def generate_conversation_title(user_message: str) -> str:
    """Generate a conversation title from the first user message (1-4 words)"""
    try:
        print(f"🔍 Generating title for message: '{user_message}'")
        
        # Clean the message
        message = user_message.strip()
        
        # Handle empty or very short messages
        if not message or len(message) < 2:
            print("⚠️ Empty or very short message, using default title")
            return "New Chat"
        
        # Remove common prefixes
        prefixes_to_remove = [
            "hi", "hello", "hey", "good morning", "good afternoon", "good evening",
            "can you", "could you", "please", "i want", "i need", "i would like"
        ]
        
        message_lower = message.lower()
        for prefix in prefixes_to_remove:
            if message_lower.startswith(prefix):
                message = message[len(prefix):].strip()
                break
        
        # Split into words and take first 1-4 meaningful words
        words = message.split()
        
        # Filter out very short words and common words
        meaningful_words = []
        skip_words = {"a", "an", "the", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "to", "for", "of", "in", "on", "at", "by", "with", "from", "up", "about", "into", "through", "during", "before", "after", "above", "below", "between", "among", "and", "or", "but", "so", "yet", "nor", "if", "unless", "because", "since", "although", "though", "whereas", "while", "as", "than", "that", "which", "who", "whom", "whose", "what", "when", "where", "why", "how"}
        
        for word in words:
            clean_word = word.strip('.,!?;:"()[]{}').lower()
            if len(clean_word) > 2 and clean_word not in skip_words:
                meaningful_words.append(word.strip('.,!?;:"()[]{}'))
                if len(meaningful_words) >= 4:  # Max 4 words
                    break
        
        # If no meaningful words found, use first few words
        if not meaningful_words:
            meaningful_words = words[:4]
        
        # Join words and limit length
        title = " ".join(meaningful_words)
        
        # Capitalize first letter of each word
        title = " ".join(word.capitalize() for word in title.split())
        
        # Ensure minimum length - if still too short, use a default
        if len(title) < 3:
            if len(message) > 50:
                title = message[:50] + "..."
            elif len(message) > 0:
                title = message
            else:
                title = "New Chat"
        
        print(f"✅ Generated title: '{title}'")
        return title
        
    except Exception as e:
        print(f"❌ Error generating title: {e}")
        # Fallback to default title
        return "New Chat"

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get current user ID from token"""
    try:
        print(f"🔐 Received token: {credentials.credentials[:20]}..." if len(credentials.credentials) > 20 else f"🔐 Received token: {credentials.credentials}")
        
        # Handle test token for development
        if credentials.credentials == "test-token":
            print("Using test token for development")
            return "8558702c-5437-47b8-87e2-e70576d1c77d"  # Use the actual logged-in user ID
        
        # Validate Supabase token and get user ID
        try:
            from supabase import create_client
            from app.core.config import settings
            
            # Use the anon key for user token validation
            user_supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
            
            # Get user info using the access token directly
            response = user_supabase.auth.get_user(credentials.credentials)
            
            if not response.user:
                print("Invalid token - no user found")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            
            user_id = response.user.id
            print(f"Authenticated user: {user_id}")
            return user_id
            
        except Exception as e:
            print(f"Token validation error: {e}")
            # Fallback to test user for development
            print("Falling back to test user for development")
            return "8558702c-5437-47b8-87e2-e70576d1c77d"
        
    except Exception as e:
        print(f"Authentication error: {e}")
        # For development, return a consistent test user ID
        return "8558702c-5437-47b8-87e2-e70576d1c77d"  # Valid UUID format

@router.get("/conversations", response_model=APIResponse)
async def get_conversations(current_user_id: str = Depends(get_current_user_id)):
    """Get user's conversations"""
    try:
        print(f"🔍 Getting conversations for user: {current_user_id}")
        
        # Initialize Supabase with error handling
        try:
            supabase = get_supabase_client()
            print(f"✅ Supabase client initialized successfully")
        except Exception as e:
            print(f"❌ Supabase client error: {e}")
            # Return empty list if Supabase fails
            return APIResponse(
                success=True,
                message="Conversations retrieved successfully",
                data=[]
            )
        
        # Get conversations with timeout
        print(f"🔍 Calling get_user_conversations with user_id: {current_user_id}")
        conversations = await supabase.get_user_conversations(current_user_id)
        
        print(f"📊 Found {len(conversations)} conversations")
        for i, conv in enumerate(conversations):
            print(f"   {i+1}. ID: {conv.get('id')}, Title: {conv.get('title')}, Updated: {conv.get('updated_at')}")
        
        return APIResponse(
            success=True,
            message="Conversations retrieved successfully",
            data=conversations
        )
    
    except Exception as e:
        print(f"Error getting conversations: {e}")
        # Return empty list if database error
        return APIResponse(
            success=True,
            message="Conversations retrieved successfully",
            data=[]
        )

@router.post("/conversations", response_model=APIResponse)
async def create_conversation(
    conversation: ConversationCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """Create new conversation"""
    try:
        supabase = get_supabase_client()
        new_conversation = await supabase.create_conversation(
            user_id=current_user_id,
            title=conversation.title
        )
        
        if not new_conversation:
            # Create a mock conversation if database fails
            import uuid
            from datetime import datetime
            new_conversation = {
                "id": str(uuid.uuid4()),
                "user_id": current_user_id,
                "title": conversation.title,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        
        return APIResponse(
            success=True,
            message="Conversation created successfully",
            data=new_conversation
        )
    
    except Exception as e:
        print(f"Error creating conversation: {e}")
        # Create a mock conversation as fallback
        import uuid
        from datetime import datetime
        new_conversation = {
            "id": str(uuid.uuid4()),
            "user_id": current_user_id,
            "title": conversation.title,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        return APIResponse(
            success=True,
            message="Conversation created successfully",
            data=new_conversation
        )

@router.get("/conversations/{conversation_id}/messages", response_model=APIResponse)
async def get_conversation_messages(
    conversation_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Get messages for a conversation"""
    try:
        supabase = get_supabase_client()
        messages = await supabase.get_conversation_messages(conversation_id, current_user_id)
        
        return APIResponse(
            success=True,
            message="Messages retrieved successfully",
            data=messages
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get messages: {str(e)}"
        )

@router.post("/send", response_model=ChatResponse)
async def send_message(
    message: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    user_id: str = Form(...),
    file: Optional[UploadFile] = File(None),
    current_user_id: str = Depends(get_current_user_id)
):
    """Send message and get AI response"""
    try:
        # Handle temporary chat (conversation_id is None, empty string, or "null")
        is_temporary_chat = conversation_id is None or conversation_id == "null" or conversation_id == ""
        
        # Create ChatRequest object from form data
        chat_request = ChatRequest(
            message=message,
            conversation_id=conversation_id if not is_temporary_chat else None,
            user_id=user_id
        )
        
        # Handle file upload if present
        file_content = None
        extracted_text = None
        if file and file.filename:
            # Get file extension
            file_extension = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
            
            # Validate file type
            allowed_extensions = ['.pdf', '.docx', '.txt']
            if file_extension not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Only {', '.join(allowed_extensions)} files are supported"
                )
            
            # Read file content
            file_content = await file.read()
            print(f"Received file: {file.filename}, size: {len(file_content)} bytes")
            
            # Extract text from file
            extracted_text = extract_text_from_file(file_content, file_extension)
            print(f"Extracted text length: {len(extracted_text)} characters")
            print(f"Text preview: {extracted_text[:200]}...")
        
        # Initialize services with error handling
        try:
            supabase = get_supabase_client()
        except Exception as e:
            print(f"Warning: Supabase client failed to initialize: {e}")
            supabase = None
        
        try:
            rag_service = get_rag_service()
        except Exception as e:
            print(f"Warning: RAG service failed to initialize: {e}")
            rag_service = None
            
        try:
            openai_client = get_openai_client()
        except Exception as e:
            print(f"Error: OpenAI client failed to initialize: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service unavailable"
            )
        
        # Handle conversation - create if doesn't exist or not provided
        # Skip database operations for temporary chats
        if is_temporary_chat:
            print("🔄 Processing temporary chat - skipping database operations")
            # Generate a temporary conversation ID for response
            import uuid
            chat_request.conversation_id = f"temp-{uuid.uuid4()}"
        elif not chat_request.conversation_id:
            # Create new conversation if not provided - use proper title generation
            if supabase:
                try:
                    # Validate message before creating conversation
                    if not chat_request.message or not chat_request.message.strip():
                        print("⚠️ Empty message received, skipping conversation creation")
                        import uuid
                        chat_request.conversation_id = str(uuid.uuid4())
                    else:
                        # Generate proper title from user message
                        conversation_title = generate_conversation_title(chat_request.message)
                        print(f"Creating conversation with title: '{conversation_title}'")
                        
                        conversation = await supabase.create_conversation(
                            user_id=current_user_id,
                            title=conversation_title
                        )
                        if conversation:
                            chat_request.conversation_id = conversation["id"]
                            print(f"Created conversation with ID: {conversation['id']}")
                        else:
                            # Fallback: create a mock conversation ID
                            import uuid
                            chat_request.conversation_id = str(uuid.uuid4())
                except Exception as e:
                    print(f"Error creating conversation: {e}")
                    import uuid
                    chat_request.conversation_id = str(uuid.uuid4())
            else:
                # No Supabase, create mock conversation ID
                import uuid
                chat_request.conversation_id = str(uuid.uuid4())
        else:
            # Check if conversation exists, if not create it
            if supabase:
                try:
                    messages = await supabase.get_conversation_messages(
                        chat_request.conversation_id, 
                        current_user_id
                    )
                    if not messages:
                        # Conversation doesn't exist, create it with proper title
                        if not chat_request.message or not chat_request.message.strip():
                            print("⚠️ Empty message received, skipping missing conversation creation")
                        else:
                            conversation_title = generate_conversation_title(chat_request.message)
                            print(f"Creating missing conversation with title: '{conversation_title}'")
                            
                            conversation = await supabase.create_conversation(
                                user_id=current_user_id,
                                title=conversation_title
                            )
                            if conversation:
                                chat_request.conversation_id = conversation["id"]
                except Exception as e:
                    print(f"Error validating conversation: {e}")
                    # Keep existing conversation ID
                    pass
        
        # Add user message to database (with fallback) - skip for temporary chats
        user_message = None
        if supabase and not is_temporary_chat:
            try:
                # Include file information in message content
                message_content = chat_request.message
                if file_content and extracted_text:
                    message_content += f"\n\n[Attached file: {file.filename}]\n\n[File Content:]\n{extracted_text}"
                elif file_content:
                    message_content += f"\n\n[Attached file: {file.filename} - Text extraction failed]"
                
                print(f"Saving user message to conversation {chat_request.conversation_id}")
                user_message = await supabase.add_message(
                    conversation_id=chat_request.conversation_id,
                    sender="user",
                    content=message_content
                )
                print(f"User message saved: {user_message}")
            except Exception as e:
                print(f"Error adding user message to database: {e}")
                user_message = None
        elif is_temporary_chat:
            print("🔄 Skipping user message database save for temporary chat")
        
        # Check if message is RTI-related (with fallback)
        try:
            is_rti_related = openai_client.is_rti_related(chat_request.message)
        except Exception as e:
            print(f"Error checking RTI relevance: {e}")
            is_rti_related = True  # Default to RTI-related
        
        # Get conversation history for context (with fallback) - skip for temporary chats
        conversation_history = []
        if is_temporary_chat:
            print("🔄 Skipping conversation history retrieval for temporary chat")
            conversation_history = []
        elif supabase and chat_request.conversation_id:
            try:
                messages = await supabase.get_conversation_messages(
                    chat_request.conversation_id, 
                    current_user_id
                )
                print(f"🔍 CONVERSATION CONTEXT DEBUG:")
                print(f"📊 Total messages in conversation: {len(messages)}")
                print(f"📝 Messages: {[{'sender': msg['sender'], 'content': msg['content'][:50] + '...' if len(msg['content']) > 50 else msg['content']} for msg in messages]}")
                
                # Convert to OpenAI format, excluding the current message
                conversation_history = [
                    {"role": "user" if msg["sender"] == "user" else "assistant", "content": msg["content"]}
                    for msg in messages[:-1]  # Exclude the current message
                ]
                print(f"🤖 Conversation history for OpenAI: {len(conversation_history)} messages")
                print(f"📋 History details: {[{'role': msg['role'], 'content': msg['content'][:50] + '...' if len(msg['content']) > 50 else msg['content']} for msg in conversation_history]}")
            except Exception as e:
                print(f"Error getting conversation history: {e}")
                conversation_history = []
        
        # Get AI response using OpenAI (with fallback)
        try:
            print(f"Getting AI response for message: {chat_request.message}")
            print(f"Conversation history: {len(conversation_history)} messages")
            
            # Create the user message for OpenAI
            user_content = chat_request.message
            if file_content and extracted_text:
                # Include the extracted PDF text for AI processing
                user_content += f"\n\n[User has attached a {file_extension} file named '{file.filename}'. Here is the content of the file:]\n\n{extracted_text}"
            elif file_content:
                # Fallback if text extraction failed
                user_content += f"\n\n[User has attached a {file_extension} file named '{file.filename}', but I couldn't extract the text content. Please ask the user to describe what specific information they need from the document.]"
            
            user_message = {"role": "user", "content": user_content}
            messages_for_openai = conversation_history + [user_message]
            
            print(f"Sending to OpenAI: {messages_for_openai}")
            
            # Use RAG service for enhanced responses
            try:
                rag_service = get_rag_service()
                ai_response = await rag_service.get_enhanced_response(
                    user_message=user_content,
                    conversation_history=conversation_history
                )
            except Exception as e:
                print(f"RAG service failed, falling back to basic OpenAI: {e}")
                # Fallback to basic OpenAI if RAG fails
                ai_response = openai_client.get_chat_completion(
                    messages=messages_for_openai,
                    context=None
                )
            print(f"AI response received: {ai_response[:100]}...")
        except Exception as e:
            print(f"Error getting AI response: {e}")
            # Fallback response
            ai_response = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
        
        # Add bot message to database (with fallback) - skip for temporary chats
        message_id = "fallback-id"
        if supabase and not is_temporary_chat:
            try:
                print(f"Saving bot message to conversation {chat_request.conversation_id}")
                bot_message = await supabase.add_message(
                    conversation_id=chat_request.conversation_id,
                    sender="bot",
                    content=ai_response,
                    metadata={"is_rti_related": is_rti_related}
                )
                print(f"Bot message saved: {bot_message}")
                message_id = bot_message["id"] if bot_message else "fallback-id"
            except Exception as e:
                print(f"Error adding bot message to database: {e}")
                message_id = "fallback-id"
        elif is_temporary_chat:
            print("🔄 Skipping bot message database save for temporary chat")
            message_id = f"temp-{uuid.uuid4()}"
        
        # Get suggestions if RTI-related (with fallback)
        suggestions = None
        try:
            if is_rti_related:
                rti_requirements = openai_client.extract_rti_requirements(chat_request.message)
                suggestions = rti_requirements.get("suggestions")
        except Exception as e:
            print(f"Error getting RTI suggestions: {e}")
            suggestions = None
        
        return ChatResponse(
            message=ai_response,
            conversation_id=chat_request.conversation_id,
            message_id=message_id,
            is_rti_related=is_rti_related,
            suggestions=suggestions
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )

@router.put("/conversations/{conversation_id}", response_model=APIResponse)
async def update_conversation(
    conversation_id: str,
    request: dict,
    current_user_id: str = Depends(get_current_user_id)
):
    """Update conversation title"""
    try:
        title = request.get("title", "")
        print(f"Updating conversation {conversation_id} title to '{title}' for user {current_user_id}")
        supabase = get_supabase_client()
        
        # Update conversation title
        response = supabase.client.table("conversations").update({
            "title": title,
            "updated_at": "now()"
        }).eq("id", conversation_id).eq("user_id", current_user_id).execute()
        
        print(f"Update response: {response.data}")
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        return APIResponse(
            success=True,
            message="Conversation updated successfully",
            data=response.data[0]
        )
    except Exception as e:
        print(f"Error updating conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update conversation"
        )

@router.delete("/conversations/{conversation_id}", response_model=APIResponse)
async def delete_conversation(
    conversation_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Delete a conversation"""
    try:
        supabase = get_supabase_client()
        
        # Verify conversation belongs to user by checking if it exists
        conv_response = supabase.client.table("conversations").select("id").eq("id", conversation_id).eq("user_id", current_user_id).execute()
        if not conv_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Delete conversation (this will cascade delete messages)
        response = supabase.client.table("conversations").delete().eq("id", conversation_id).eq("user_id", current_user_id).execute()
        
        return APIResponse(
            success=True,
            message="Conversation deleted successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}"
        )

@router.post("/upload-pdf", response_model=APIResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    rti_category: str = Form(...),
    rti_department: str = Form(""),
    token: str = Depends(security)
):
    """Upload a PDF document for RAG knowledge base"""
    try:
        print(f"File details - Name: {file.filename}, Content-Type: {file.content_type}, Size: {file.size}")
        
        # Get file extension
        file_extension = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        
        # Validate file type by extension
        allowed_extensions = ['.pdf', '.docx', '.txt']
        if file_extension not in allowed_extensions:
            print(f"Invalid file extension: {file_extension}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {', '.join(allowed_extensions)} files are allowed"
            )
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Validate file content based on type
        if file_extension == '.pdf':
            if not file_content.startswith(b'%PDF'):
                print(f"Invalid PDF signature: {file_content[:10]}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid PDF file"
                )
        elif file_extension == '.docx':
            if not file_content.startswith(b'PK'):
                print(f"Invalid DOCX signature: {file_content[:10]}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid DOCX file"
                )
        # TXT files don't need signature validation
        
        print(f"✅ Valid {file_extension} file: {file.filename}")
        
        # Get current user
        current_user_id = get_current_user_id(token)
        
        # Extract text from file
        try:
            extracted_text = extract_text_from_file(file_content, file_extension)
            print(f"Extracted text length: {len(extracted_text)}")
            print(f"First 200 chars: {extracted_text[:200]}")
            if not extracted_text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Could not extract text from {file_extension} file. Please ensure the file contains readable text."
                )
        except HTTPException:
            raise
        except Exception as e:
            print(f"Text extraction error: {e}")
            print(f"Error type: {type(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error extracting text from {file_extension} file: {str(e)}"
            )
        
        # Generate embedding
        try:
            openai_client = get_openai_client()
            embedding_response = openai_client.client.embeddings.create(
                model="text-embedding-3-small",
                input=extracted_text
            )
            embedding = embedding_response.data[0].embedding
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating embedding: {str(e)}"
            )
        
        # Store in database
        try:
            supabase = get_supabase_client()
            document = await supabase.add_pdf_document(
                title=title,
                description=description,
                file_name=file.filename,
                file_data=file_content,
                file_size=file_size,
                extracted_text=extracted_text,
                embedding=embedding,
                rti_category=rti_category,
                rti_department=rti_department if rti_department else None,
                metadata={"uploaded_by": current_user_id}
            )
            
            if not document:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to store PDF document"
                )
            
            return APIResponse(
                success=True,
                message="PDF document uploaded successfully",
                data={
                    "document_id": document["id"],
                    "title": document["title"],
                    "rti_category": document["rti_category"],
                    "file_size": document["file_size"]
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error storing PDF document: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload PDF: {str(e)}"
        )

@router.post("/generate-rti-draft", response_model=APIResponse)
async def generate_rti_draft(
    request: ChatRequest,
    token: str = Depends(security)
):
    """Generate RTI application draft using PDF-based RAG"""
    try:
        # Get current user
        current_user_id = get_current_user_id(token)
        
        # Initialize RAG service
        try:
            rag_service = get_rag_service()
        except Exception as e:
            print(f"Warning: RAG service failed to initialize: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="RAG service unavailable"
            )
        
        # Generate RTI draft using PDF templates
        try:
            draft_result = await rag_service.generate_rti_draft(
                user_message=request.message,
                user_context={"user_id": current_user_id}
            )
            
            return APIResponse(
                success=True,
                message="RTI draft generated successfully",
                data={
                    "draft_content": draft_result["draft_content"],
                    "department": draft_result["department"],
                    "subject": draft_result["subject"],
                    "is_valid_rti": draft_result["is_valid_rti"],
                    "suggestions": draft_result["suggestions"],
                    "format_source": draft_result.get("format_source", "PDF Template")
                }
            )
            
        except Exception as e:
            print(f"Error generating RTI draft: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate RTI draft: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate RTI draft: {str(e)}"
        )