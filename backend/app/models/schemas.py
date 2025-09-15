"""
Pydantic models for API request/response schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MessageSender(str, Enum):
    USER = "user"
    BOT = "bot"

class RTIStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    FILED = "filed"
    REJECTED = "rejected"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class FilingStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    REJECTED = "rejected"

# User Models
class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserProfile(UserProfileBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Conversation Models
class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0

    class Config:
        from_attributes = True

# Message Models
class MessageBase(BaseModel):
    sender: MessageSender
    content: str
    metadata: Optional[Dict[str, Any]] = {}

class MessageCreate(MessageBase):
    conversation_id: str

class Message(MessageBase):
    id: str
    conversation_id: str
    created_at: datetime

    class Config:
        from_attributes = True

# RTI Draft Models
class RTIDraftBase(BaseModel):
    title: str
    content: str
    department: Optional[str] = None
    subject: Optional[str] = None

class RTIDraftCreate(RTIDraftBase):
    pass

class RTIDraftUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    department: Optional[str] = None
    subject: Optional[str] = None
    status: Optional[RTIStatus] = None

class RTIDraft(RTIDraftBase):
    id: str
    user_id: str
    conversation_id: Optional[str] = None
    status: RTIStatus
    application_number: Optional[str] = None
    filing_fee: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# RTI Filing Models
class RTIFilingBase(BaseModel):
    rti_draft_id: str
    pio_email: Optional[str] = None
    pio_address: Optional[str] = None

class RTIFilingCreate(RTIFilingBase):
    pass

class RTIFilingUpdate(BaseModel):
    payment_id: Optional[str] = None
    payment_status: Optional[PaymentStatus] = None
    filing_status: Optional[FilingStatus] = None
    application_number: Optional[str] = None
    submission_date: Optional[datetime] = None
    acknowledgment_date: Optional[datetime] = None
    response_date: Optional[datetime] = None

class RTIFiling(RTIFilingBase):
    id: str
    user_id: str
    payment_id: Optional[str] = None
    payment_status: PaymentStatus
    filing_status: FilingStatus
    application_number: Optional[str] = None
    submission_date: Optional[datetime] = None
    acknowledgment_date: Optional[datetime] = None
    response_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Chat Models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: str

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    message_id: str
    is_rti_related: bool
    suggestions: Optional[str] = None

class RTIDraftRequest(BaseModel):
    message: str
    user_id: str
    conversation_id: Optional[str] = None

class RTIDraftResponse(BaseModel):
    draft_content: str
    department: str
    subject: str
    is_valid_rti: bool
    suggestions: Optional[str] = None
    rti_draft_id: Optional[str] = None

# Knowledge Base Models
class KnowledgeBaseItem(BaseModel):
    id: str
    title: str
    content: str
    source_url: Optional[str] = None
    category: Optional[str] = None
    similarity: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

# API Response Models
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
