from fastapi import APIRouter, Header, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from app.schemas import Task
from app.utlis import decode_token, get_discord_user
from app.database import get_db
from app.discord_hooks import CreateMessage
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/task"
)


@router.post("/")
async def create_task(task: Task, auth_token:Annotated[str | None, Header()] = None, db: Session = Depends(get_db) ):
    print(auth_token)
    if not auth_token:
        return JSONResponse(status_code=401, content={"msg":"Unauthorized"})
    
    user_email = await decode_token(auth_token)
    
    if user_email:
        user = get_discord_user(db, user_email)
        if user:
            message = CreateMessage(title=task.title, description=task.description, scope_of_work=task.scope_of_work,compensation=task.compensation,deadline=task.deadline, resources=task.resources)
    
            message.send(url=user.webhook_url)
            return JSONResponse(status_code=200, content={"msg":"posted"})
        
    return JSONResponse(status_code=401, content={"msg":"Unauthorized"})