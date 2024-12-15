from fastapi import APIRouter, Request
from app.services.workflow_manager import WorkflowManager

router = APIRouter()
workflow_manager = WorkflowManager()

@router.post('/api/workflow')
async def handle_workflow(request: Request):
    data = await request.json()
    task_config = data.get('task_config')
    result = workflow_manager.execute(task_config)
    return {'result': result}
