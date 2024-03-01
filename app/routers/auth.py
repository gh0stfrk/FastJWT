from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from ..utlis import authenticate_user, create_access_token, decode_token, get_user
from ..schemas import UserData, UserInDB
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Annotated

authentication_router = APIRouter(
    prefix="/auth",
    tags=["authentication"],)


async def get_current_user(db:Session = Depends(get_db), auth_token: Annotated[str | None, Header()] = None):
    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"Jwt-Token": ""},)
        
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"Jwt-Token": ""},)
    
    email: str = await decode_token(auth_token)
    
    if email:
        user = get_user(db, email)
        return user
    
    raise token_exception


@authentication_router.post("")
async def login_for_access_token(user: UserData):
    db : Session = next(get_db())
    
    if user.email and user.password:
        user = authenticate_user(db, user.email, user.password)
        
        if user:
            token = create_access_token(data={"sub": user.email})
            print(token)
            return JSONResponse({"token": token, "email": user.email}, status_code=200)
        
    return JSONResponse({"message": "Invalid credentials"}, status_code=403)

