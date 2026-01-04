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
    except ValueError as e:
         raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    return user
