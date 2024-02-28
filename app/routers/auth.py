from fastapi import APIRouter
from ..utlis import authenticate_user, create_access_token
from ..schemas import UserData
from ..database import get_db
from sqlalchemy.orm import Session

authentication_router = APIRouter(
    prefix="/auth",
    tags=["authentication"],)


@authentication_router.post("")
async def root(user: UserData):
    db : Session = next(get_db())
    # pass the email and password the util func
    print(user)
    if user.email and user.password:
        user = authenticate_user(db, user.email, user.password)
        if user:
            token = create_access_token(data={"sub": user.email})
            return {"token": token}
    # if user is real, return a jwt token
    # else return an error message
    return {"message": "Go away you stinky hacker"}

