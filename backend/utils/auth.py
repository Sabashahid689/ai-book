from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get secret key from environment, use a default if not set (development only)
SECRET_KEY = os.getenv("SECRET_KEY") or "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """Verify an access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        return token_data
    except jwt.PyJWTError:
        return None


def authenticate_user(username: str, password: str) -> Optional[TokenData]:
    """
    Authenticate a user by username and password.
    
    Note: This is a simplified implementation. In a real application, 
    you would look up the user in a database.
    """
    # For now, let's implement a simple check
    # In a real application, you would look up the user in a database
    # and verify the password against the stored hash
    
    # Placeholder for a valid user
    if username == "user" and password == "password":  # Replace with actual user lookup
        return TokenData(username=username)
    
    return None