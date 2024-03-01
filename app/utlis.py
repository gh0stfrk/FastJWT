from .models import User
from datetime import timedelta, datetime
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password, hashed_password) -> bool:
    """Verify password
    Args:
        plain_password (str): password
        hashed_password (str): hashed password
    Returns:
        bool: True if password is correct, False otherwise. 
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password) -> str:
    """
    Hash a given password 
    Args:
        password (str): password
    Returns:
        str: hashed password
    """
    return pwd_context.hash(password)


def get_user(db:Session, email:str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    return user


def authenticate_user(db:Session , email:str, password:str) -> User | bool:
    """
    Authenticates user
    Args:
        db (Session): database session
        email (str): user email
        password (str): user password
    Returns:
        User | bool: user object if authentication is successful, False otherwise. 
    """
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data:dict, expires_delta:timedelta | None = None):
    """
    Create a JWT token
    Args:
        data (dict): data to be encoded
        expires_delta (timedelta | None, optional): expiration time. Defaults to None.
    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(token: str, key: str | None = None) -> str | None:
    """
    Decode a JWT token
    
    Args:
        token (str): JWT token
        key (str | None, optional): key to extract from the token. Defaults to None.
        
    Returns:
        str | None: extracted data from the token or None if token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if key:
            return payload.get(key)
        return payload.get('sub')
    except JWTError:
        return None
