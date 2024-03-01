from fastapi import APIRouter, Depends, Header
from typing import Annotated

from fastapi.responses import JSONResponse
from .auth import get_current_user
from ..schemas import UserInDB

from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    prefix="/protected"
)

@router.get("")
async def protected_endpoint(user: UserInDB = Depends(get_current_user)):
    return JSONResponse(
        {"message": "This is a protected endpoint",
            "email": user.email,}, status_code=200
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/test")
async def test(frank_fruit: Annotated[str| None, Header()], nerd_thing: Annotated[str | None, Header()]):
    print(nerd_thing)
    return JSONResponse(
        {"message": "This is a protected endpoint",
         "header":frank_fruit}, status_code=200
    )