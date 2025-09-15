"""
User profile endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.schemas import (
    UserProfile, UserProfileUpdate, APIResponse, ErrorResponse
)
from app.services.supabase_client import get_supabase_client

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

@router.get("/me", response_model=APIResponse)
async def get_my_profile(current_user_id: str = Depends(get_current_user_id)):
    """Get current user's profile"""
    try:
        supabase = get_supabase_client()
        profile = await supabase.get_user_profile(current_user_id)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        return APIResponse(
            success=True,
            message="Profile retrieved successfully",
            data=profile
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile: {str(e)}"
        )

@router.put("/me", response_model=APIResponse)
async def update_my_profile(
    profile_update: UserProfileUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    """Update current user's profile"""
    try:
        supabase = get_supabase_client()
        
        # Convert Pydantic model to dict, excluding None values
        update_data = profile_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        updated_profile = await supabase.update_user_profile(current_user_id, update_data)
        
        if not updated_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        return APIResponse(
            success=True,
            message="Profile updated successfully",
            data=updated_profile
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )

@router.delete("/me", response_model=APIResponse)
async def delete_my_profile(current_user_id: str = Depends(get_current_user_id)):
    """Delete current user's profile (this will cascade delete all user data)"""
    try:
        supabase = get_supabase_client()
        
        # Delete user profile (this will cascade delete all related data)
        response = supabase.client.table("profiles").delete().eq("id", current_user_id).execute()
        
        return APIResponse(
            success=True,
            message="Profile deleted successfully"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete profile: {str(e)}"
        )
