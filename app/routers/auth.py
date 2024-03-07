from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from fastapi.responses import JSONResponse
from ..utlis import authenticate_user, create_access_token, create_refresh_token, decode_token, get_user, get_user_by_id, hash_password, authenticate_discord_user
from ..schemas import UserData, DiscordUserSchema
from ..database import get_db
from ..models import DiscordUser
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated

authentication_router = APIRouter(
    prefix="/auth",
    tags=["authentication"],)


async def check_cookie(request: Request):
    cookie = request.cookies
    if not cookie:
        return None
    if cookie.get('refresh-Token'):
        return cookie.get('refresh-Token')

async def get_current_user(db:Session = Depends(get_db), auth_token: Annotated[str | None, Header()] = None):
    """
    Get current user's details from an authentication token
    Args:
        db (Session): database session
        auth_token (str | None): authentication token
    Returns:
        User
    """
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"Jwt-Token": ""},)   
    if not auth_token:
        raise token_exception
    email: str = await decode_token(auth_token)
    if email:
        user = get_user(db, email)
        return user
    raise token_exception


@authentication_router.get("/cookie")
async def get_cookie(cookie: str = Depends(check_cookie)):
    content = {"message":"Cookie is accepted"}
    response = JSONResponse(content=content)
    response.set_cookie(key="test-Cookie", value="ChoclateChip")
    return response


@authentication_router.post("")
async def login_for_access_token(user: UserData):
    """
    Login for access token
    """
    # Explicitly yeilding a db session 
    # Instead of using Depends(), [just for fun]
    db : Session = next(get_db())
    if user.email and user.password:
        user = authenticate_discord_user(db, user.email, user.password)
        if user:
            token = create_access_token(data={"sub": user.email})
            refresh_token = create_refresh_token(data={"id": user.id })            
            response = JSONResponse({"token": token, "email": user.email}, status_code=200)
            response.set_cookie(key="refresh-Token", value=refresh_token)
            return response       
    return JSONResponse({"message": "Invalid credentials"}, status_code=403)


@authentication_router.post("/refresh")
async def refresh_token(refresh_token: str = Depends(check_cookie), db: Session = Depends(get_db)):
    """
    Create a refresh token route
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    decoded_token = await decode_token(refresh_token, 'id', type='refresh')
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = get_user_by_id(db, decoded_token)
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")
    access_token = create_access_token(data={"sub": user.email})
    return JSONResponse({"token": access_token, "email": user.email}, status_code=200)


@authentication_router.post('/signup')
async def signup(user: DiscordUserSchema, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    if user:
        try:
            new_user = DiscordUser(name=user.name, email=user.email, webhook_url=user.webhookUrl, hashed_password=hash_password(user.password))
            db.add(new_user)
            db.commit()
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")
        return JSONResponse({"message": "User created successfully", "email":user.email}, status_code=201)
    
    return JSONResponse({"message": "User not created"}, status_code=400)
