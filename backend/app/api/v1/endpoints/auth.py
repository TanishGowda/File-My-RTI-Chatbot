"""
Authentication endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.schemas import APIResponse, ErrorResponse
from app.services.supabase_client import get_supabase_client
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

@router.get("/verify", response_model=APIResponse)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and get user info"""
    try:
        supabase = get_supabase_client()
        
        # Verify token with Supabase
        response = supabase.client.auth.get_user(credentials.credentials)
        
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get user profile
        profile = await supabase.get_user_profile(response.user.id)
        
        if not profile:
            # Create profile if it doesn't exist
            profile = await supabase.create_user_profile(
                user_id=response.user.id,
                email=response.user.email,
                full_name=response.user.user_metadata.get("full_name")
            )
        
        return APIResponse(
            success=True,
            message="Token verified successfully",
            data={
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "profile": profile
                }
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}"
        )

@router.post("/refresh", response_model=APIResponse)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh JWT token"""
    try:
        supabase = get_supabase_client()
        
        # Refresh token with Supabase
        response = supabase.client.auth.refresh_session(credentials.credentials)
        
        if not response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token refresh failed"
            )
        
        return APIResponse(
            success=True,
            message="Token refreshed successfully",
            data={
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "expires_at": response.session.expires_at
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token refresh failed: {str(e)}"
        )

@router.post("/logout", response_model=APIResponse)
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user"""
    try:
        supabase = get_supabase_client()
        
        # Sign out user
        supabase.client.auth.sign_out()
        
        return APIResponse(
            success=True,
            message="Logged out successfully"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )
