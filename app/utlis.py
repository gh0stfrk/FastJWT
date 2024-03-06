from .models import User, DiscordUser
from datetime import timedelta, datetime
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_SECRET_KEY


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
    """
    Get user by email
    Args:
        db (Session): database session
        email (str): user email
    Returns:
        User | None: user object if user exists, None otherwise.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    return user

def get_user_by_id(db:Session, id:int) -> User | None:
    """
    Get user by id
    Args:
        db (Session): database session
        id (int): user id
    Returns:
        User | None: user object if user exists, None otherwise (if user does not exist in the database, return None)
    """
    user = db.query(User).filter(User.id == id).first()
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
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a refresh token
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
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(token: str, key: str | None = None, type: str = 'access') -> str | None:
    """
    Decode a JWT token
    
    Args:
        token (str): JWT token
        key (str | None, optional): key to extract from the token. Defaults to None.
        type (str, optional): type of token [refresh or access]
    Returns:
        str | None: extracted data from the token or None if token is invalid.
    """
    try:
        if type == 'refresh':
            payload = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        else:    
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])     
        if key:
            return payload.get(key)
        return payload.get('sub')
    except JWTError as e:
        print(e)
        return None

def get_discord_user(db: Session, email: str) -> DiscordUser | None:
    """
    Get Discord user by email

    Args:
        db (Session): Database session
        email (str): User email

    Returns:
        DiscordUser | None: Discord user object if user exists, None otherwise.
    """
    discord_user = db.query(DiscordUser).filter(DiscordUser.email == email).first()
    if not discord_user:
        return None
    return discord_user

def authenticate_discord_user(db: Session, email: str, password: str) -> DiscordUser | bool:
    """
    Authenticate Discord user

    Args:
        db (Session): Database session
        email (str): User email
        password (str): User password

    Returns:
        DiscordUser | bool: Discord user object if authentication is successful, False otherwise.
    """
    discord_user = get_discord_user(db, email)
    if not discord_user:
        return False
    if discord_user.password != password:
        return False
    return discord_user