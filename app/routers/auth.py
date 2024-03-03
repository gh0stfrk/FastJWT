from fastapi import APIRouter, Depends, HTTPException, Header, Request, status, Cookie
from fastapi.responses import JSONResponse
from ..utlis import authenticate_user, create_access_token, create_refresh_token, decode_token, get_user, get_user_by_id
from ..schemas import UserData
from ..database import get_db
from sqlalchemy.orm import Session
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
    # Explicitly yeilding a db session 
    # Instead of using Depends(), [just for fun]
    db : Session = next(get_db())
    
    if user.email and user.password:
        user = authenticate_user(db, user.email, user.password)
        
        if user:
            token = create_access_token(data={"sub": user.email})
            refresh_token = create_refresh_token(data={"id": user.id })
            
            response = JSONResponse({"token": token, "email": user.email}, status_code=200)
            response.set_cookie(key="refresh-Token", value=refresh_token)
            return response
        
    return JSONResponse({"message": "Invalid credentials"}, status_code=403)


@authentication_router.post("/refresh")
async def refresh_token(refresh_token: str = Depends(check_cookie), db: Session = Depends(get_db)):
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