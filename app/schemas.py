from pydantic import BaseModel


class UserData(BaseModel):
    email: str
    password: str
    
class DiscordUserSchema(BaseModel):
    email: str
    name: str
    webhookUrl: str
    password: str
    
    
class UserInDB(UserData):
    hashed_password: str
    id: int
    is_active: bool
    email: str
    
    
class Task(BaseModel):
    title: str
    description: str
    scope_of_work: str
    deadline: str
    compensation: str
    resources: str