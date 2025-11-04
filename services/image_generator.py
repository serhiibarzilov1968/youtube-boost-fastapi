from fastapi import APIRouter
from pydantic import BaseModel

class ImageRequest(BaseModel):
    title: str
    description: str

router = APIRouter(
    prefix="/api/v1/image_generator",
    tags=["image_generator"]
)

@router.post("/generate")
def generate_image(request: ImageRequest):
    # Заглушка для генератора изображений
    return {
        "message": "Image generation is not yet implemented",
        "title": request.title,
        "description": request.description
    }

