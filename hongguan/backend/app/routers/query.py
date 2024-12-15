from fastapi import APIRouter, Request, Depends
from app.services.ai_engine import AIEngine
from app.services.visualization import VisualizationService
from app.utils.security import authenticate_user
import ray

router = APIRouter()

ai_engine = AIEngine.remote()
visualization_service = VisualizationService()

@router.post('/api/query')
async def handle_query(request: Request, user=Depends(authenticate_user)):
    data = await request.json()
    user_query = data.get('query')
    insights_ref = ai_engine.process_query.remote(user_query)
    insights = await ray.get(insights_ref)
    visualization_data = visualization_service.generate(insights)
    return {'data': insights, 'visualization': visualization_data}
