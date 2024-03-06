"""
Main module
"""
from app.models import User
from app.schemas import UserData
from sqlalchemy.orm import Session
from app.utlis import hash_password
from fastapi import Depends, FastAPI
from app.routers import auth, protected, task
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from app.database import Base, engine, get_db

from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.authentication_router)
app.include_router(protected.router)
app.include_router(task.router)
Base.metadata.create_all(engine)

@app.get("/", tags=["root"])
async def root():
    return {
        "base": "Welcome to API base"
    }
    
    
@app.get("/fill_dummy")
async def fill_dummy_data():
    """
    Fill the database with dummy test users
    [ps don't use it in production]
    """
    db : Session = next(get_db())
    users = [
        {"email":"kevin@fast.com", "password":"supersecretpassword"},
        {"email":"patrick@fast.com", "password":"anotherpassword"},
        {"email":"house@fast.com", "password":"youcannotguessthis"},
        {"email":"lisbon@fast.com", "password":"password"},
    ]
    for u in users:
        try:
            new_user = User(email=u['email'], hashed_password=hash_password(u['password']))
            db.add(new_user)
            db.commit()
        except IntegrityError:
            return JSONResponse({"message":"Users already exists", "users": users}, status_code=201)
        except Exception as e:
            return JSONResponse({"status":"failed", "error":f"{e}"}, status_code=500)
    return {"message": "Dummy users added",
            "status":"success",
            "users": users}
    
@app.post("/create_user")
async def create_user(user: UserData, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    try:
        new_user = User(email=user.email, hashed_password=hash_password(user.password))
        db.add(new_user)
        db.commit()
    except IntegrityError:
        return JSONResponse({"message":f"User with {user.email} email already exists",}, status_code=201)
    except Exception as e:
        return JSONResponse({"status":"failed", "error":f"{e}"}, status_code=500)
    return {"message": "User created",
            "status":"success"}
    