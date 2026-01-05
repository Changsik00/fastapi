from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api import deps
from app.domain.models.user import Token, UserCreate, UserResponse, User, PasswordChangeRequest, PasswordRecoverRequest, PasswordResetRequest
from app.domain.repository_interfaces.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: UserRepository = Depends(deps.get_user_repo),
    auth_service: AuthService = Depends(deps.get_auth_service),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    token = await auth_service.login(user_repo=user_repo, form_data=form_data)
        
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}

@router.post("/signup", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    user_repo: UserRepository = Depends(deps.get_user_repo),
    auth_service: AuthService = Depends(deps.get_auth_service),
) -> Any:
    """
    Create new user without the need to be logged in
    """
    try:
        user = await auth_service.signup(user_repo=user_repo, user_create_data=user_in)
    except ValueError:
         raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    return user

@router.post("/password/change", response_model=UserResponse)
async def change_password(
    body: PasswordChangeRequest,
    current_user: User = Depends(deps.get_current_user),
    user_repo: UserRepository = Depends(deps.get_user_repo),
    auth_service: AuthService = Depends(deps.get_auth_service),
) -> Any:
    """
    Change password for logged-in user
    """
    try:
        return await auth_service.change_password(
            user_repo=user_repo,
            user=current_user,
            current_password=body.current_password,
            new_password=body.new_password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post("/password/recover", response_model=dict)
async def recover_password(
    body: PasswordRecoverRequest,
    user_repo: UserRepository = Depends(deps.get_user_repo),
    auth_service: AuthService = Depends(deps.get_auth_service),
) -> Any:
    """
    Password Recovery (Email Reset) - Step 1
    """
    user = await user_repo.get_by_email(email=body.email)
    
    # Security: Always return success even if email not found to prevent enumeration
    if not user:
        return {"message": "If this email exists in our system, you will receive a reset instruction."}
    
    reset_token = auth_service.create_password_reset_token(email=body.email)
    
    # TODO: Send email via SMTP
    # For MVP, we print token to console/log
    print(f"========================================")
    print(f"[MOCK EMAIL] To: {body.email}")
    print(f"Subject: Password Reset")
    print(f"Token: {reset_token}")
    print(f"========================================")
    
    # DEV ONLY: Return token in response for testing without email
    # WARNING: Remove this in production!
    return {
        "message": "If this email exists in our system, you will receive a reset instruction.",
        "reset_token": reset_token  # <--- DEV ONLY
    }

@router.post("/password/reset", response_model=UserResponse)
async def reset_password(
    body: PasswordResetRequest,
    user_repo: UserRepository = Depends(deps.get_user_repo),
    auth_service: AuthService = Depends(deps.get_auth_service),
) -> Any:
    """
    Reset Password using Token - Step 2
    """
    try:
        return await auth_service.reset_password(
            user_repo=user_repo,
            token=body.token,
            new_password=body.new_password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
