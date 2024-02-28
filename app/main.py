from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.schemas import UserData
from .routers import auth
from .database import Base, engine, get_db
from .models import User
from sqlalchemy.orm import Session
from .utlis import hash_password

app = FastAPI()
app.include_router(auth.authentication_router)

Base.metadata.create_all(engine)

@app.get("/", tags=["root"])
async def root():
    return {
        "base": "Welcome to API base"
    }
    
@app.get("/fill")
async def fill_dummy_data(users: UserData):
    db : Session = next(get_db())
    
    if users:
        user = User(email=users.email, hashed_password=hash_password(users.password))
        db.add(user)
        db.commit()
        return JSONResponse({"status":"success", "message":"Dummy data added"}, status_code=201)  
          
    users = [
        {"email":"newmail@gmail.com", "password":"supersecretpassword"},
        {"email":"kevi@gmail.com", "password":"anotherpassword"},
        {"email":"balli@gmail.com", "password":"youcannotguessthis"},
        {"email":"fastap@gmail.com", "password":"password"},
    ]
    
    user = [User(email=e["email"], hashed_password=hash_password(e["password"])) for e in users]
    
    for u in user:
        try:
            db.add(u)
            db.commit()
        except Exception as e:
            return JSONResponse({"status":"failed", "error":f"{e}"}, status_code=500)
    
    return {"message": "Dummy users added"}