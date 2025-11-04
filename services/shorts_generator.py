from fastapi import APIRouter
from pydantic import BaseModel

class ShortsRequest(BaseModel):
    video_id: str
    duration: int

router = APIRouter(
    prefix="/api/v1/shorts_generator",
    tags=["shorts_generator"]
)

@router.post("/generate")
def generate_shorts(request: ShortsRequest):
    # Заглушка для генератора шортсов
    return {
        "message": "Shorts generation is not yet implemented",
        "video_id": request.video_id,
        "duration": request.duration
    }

