"""
RTI (Right to Information) endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from app.models.schemas import (
    RTIDraft, RTIDraftCreate, RTIDraftUpdate, RTIDraftRequest, RTIDraftResponse,
    RTIFiling, RTIFilingCreate, RTIFilingUpdate, APIResponse
)
from app.services.supabase_client import get_supabase_client
from app.services.rag_service import get_rag_service
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get current user ID from token"""
    try:
        supabase = get_supabase_client()
        response = supabase.client.auth.get_user(credentials.credentials)
        
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return response.user.id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

@router.post("/generate-draft", response_model=RTIDraftResponse)
async def generate_rti_draft(
    draft_request: RTIDraftRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """Generate RTI draft using AI"""
    try:
        supabase = get_supabase_client()
        rag_service = get_rag_service()
        
        # Generate RTI draft using RAG
        draft_result = await rag_service.generate_rti_draft(
            user_message=draft_request.message,
            user_context={"user_id": current_user_id}
        )
        
        # Save draft to database
        rti_draft = await supabase.create_rti_draft(
            user_id=current_user_id,
            title=draft_result["subject"],
            content=draft_result["draft_content"],
            department=draft_result["department"],
            subject=draft_result["subject"]
        )
        
        return RTIDraftResponse(
            draft_content=draft_result["draft_content"],
            department=draft_result["department"],
            subject=draft_result["subject"],
            is_valid_rti=draft_result["is_valid_rti"],
            suggestions=draft_result["suggestions"],
            rti_draft_id=rti_draft["id"] if rti_draft else None
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate RTI draft: {str(e)}"
        )

@router.get("/drafts", response_model=APIResponse)
async def get_rti_drafts(current_user_id: str = Depends(get_current_user_id)):
    """Get user's RTI drafts"""
    try:
        supabase = get_supabase_client()
        drafts = await supabase.get_user_rti_drafts(current_user_id)
        
        return APIResponse(
            success=True,
            message="RTI drafts retrieved successfully",
            data=drafts
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get RTI drafts: {str(e)}"
        )

@router.get("/drafts/{draft_id}", response_model=APIResponse)
async def get_rti_draft(
    draft_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Get specific RTI draft"""
    try:
        supabase = get_supabase_client()
        
        # Get draft and verify ownership
        response = supabase.client.table("rti_drafts").select("*").eq("id", draft_id).eq("user_id", current_user_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RTI draft not found"
            )
        
        return APIResponse(
            success=True,
            message="RTI draft retrieved successfully",
            data=response.data[0]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get RTI draft: {str(e)}"
        )

@router.put("/drafts/{draft_id}", response_model=APIResponse)
async def update_rti_draft(
    draft_id: str,
    draft_update: RTIDraftUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    """Update RTI draft"""
    try:
        supabase = get_supabase_client()
        
        # Convert Pydantic model to dict, excluding None values
        update_data = draft_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Update draft and verify ownership
        response = supabase.client.table("rti_drafts").update(update_data).eq("id", draft_id).eq("user_id", current_user_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RTI draft not found"
            )
        
        return APIResponse(
            success=True,
            message="RTI draft updated successfully",
            data=response.data[0]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update RTI draft: {str(e)}"
        )

@router.delete("/drafts/{draft_id}", response_model=APIResponse)
async def delete_rti_draft(
    draft_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Delete RTI draft"""
    try:
        supabase = get_supabase_client()
        
        # Delete draft and verify ownership
        response = supabase.client.table("rti_drafts").delete().eq("id", draft_id).eq("user_id", current_user_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RTI draft not found"
            )
        
        return APIResponse(
            success=True,
            message="RTI draft deleted successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete RTI draft: {str(e)}"
        )

@router.post("/file", response_model=APIResponse)
async def file_rti(
    filing_request: RTIFilingCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """File RTI application (paid service)"""
    try:
        supabase = get_supabase_client()
        
        # Verify RTI draft belongs to user
        draft_response = supabase.client.table("rti_drafts").select("*").eq("id", filing_request.rti_draft_id).eq("user_id", current_user_id).execute()
        
        if not draft_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RTI draft not found"
            )
        
        # Create RTI filing record
        filing_data = {
            "user_id": current_user_id,
            "rti_draft_id": filing_request.rti_draft_id,
            "pio_email": filing_request.pio_email,
            "pio_address": filing_request.pio_address,
            "filing_fee": settings.RTI_FILING_FEE
        }
        
        response = supabase.client.table("rti_filings").insert(filing_data).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create RTI filing"
            )
        
        return APIResponse(
            success=True,
            message="RTI filing created successfully. Payment processing will be initiated.",
            data=response.data[0]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to file RTI: {str(e)}"
        )

@router.get("/filings", response_model=APIResponse)
async def get_rti_filings(current_user_id: str = Depends(get_current_user_id)):
    """Get user's RTI filings"""
    try:
        supabase = get_supabase_client()
        
        response = supabase.client.table("rti_filings").select("*").eq("user_id", current_user_id).order("created_at", desc=True).execute()
        
        return APIResponse(
            success=True,
            message="RTI filings retrieved successfully",
            data=response.data
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get RTI filings: {str(e)}"
        )

@router.get("/filings/{filing_id}", response_model=APIResponse)
async def get_rti_filing(
    filing_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Get specific RTI filing"""
    try:
        supabase = get_supabase_client()
        
        response = supabase.client.table("rti_filings").select("*").eq("id", filing_id).eq("user_id", current_user_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RTI filing not found"
            )
        
        return APIResponse(
            success=True,
            message="RTI filing retrieved successfully",
            data=response.data[0]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get RTI filing: {str(e)}"
        )
