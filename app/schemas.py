from pydantic import BaseModel


class UserData(BaseModel):
    email: str
    password: str
    

class UserInDB(UserData):
    hashed_password: str
    id: int
    is_active: bool
    email: str
    
    
