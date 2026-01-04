from datetime import timedelta
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api import deps
from app.core.config import settings
from app.domain.models.user import User, UserRole
from app.domain.repository_interfaces.user_repository import UserRepository
from app.services.auth_service import AuthService
from pydantic import BaseModel, EmailStr

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: UserRole

@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: UserRepository = Depends(deps.get_user_repo),
    auth_service: AuthService = Depends(deps.get_auth_service),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_repo.get_by_email(email=form_data.username)
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    user_repo: UserRepository = Depends(deps.get_user_repo),
    auth_service: AuthService = Depends(deps.get_auth_service),
) -> Any:
    """
    Create new user without the need to be logged in
    """
    user = await user_repo.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    
    hashed_password = auth_service.get_password_hash(user_in.password)
    user_create = User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role,
        is_active=True,
    )
    user = await user_repo.create(user=user_create)
    return user
