from datetime import timedelta
from app.services.auth_service import AuthService
from app.core.config import settings
from jose import jwt

def test_hash_password():
    service = AuthService()
    password = "secret-password"
    hashed = service.get_password_hash(password)
    assert hashed != password
    assert service.verify_password(password, hashed)
    assert not service.verify_password("wrong-password", hashed)

def test_create_access_token():
    service = AuthService()
    email = "test@example.com"
    token = service.create_access_token(subject=email)
    
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == email
    assert "exp" in payload
