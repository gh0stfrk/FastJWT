from fastapi import APIRouter
from app.schemas import Task
from app.discord_hooks import CreateMessage

router = APIRouter(
    prefix="/task"
)


@router.post("/")
async def create_task(task: Task):
    print(task)
    message = CreateMessage(title=task.title, description=task.description, scope_of_work=task.scope_of_work,compensation=task.compensation,deadline=task.deadline, resources=task.resources)
     
    message.send(url="https://discord.com/api/webhooks/1214543877562703972/0KZjD9mDn7Yx5ZzVLDdzy_lBUZE0npMXPf8jfkDJXwOOS-CThEPH2eYury391TegDx75")
    
    return {"msg":"posted"}