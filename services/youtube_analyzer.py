from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY":
    print("WARNING: YOUTUBE_API_KEY is not set in .env file. Using a mock response.")
    YOUTUBE_API_KEY = None # Установим None, чтобы использовать заглушку

# Модель для ответа API
class ChannelAnalysis(BaseModel):
    channel_id: str
    channel_title: str
    subscriber_count: int
    video_count: int
    view_count: int
    status: str

router = APIRouter(
    prefix="/api/v1/analyzer",
    tags=["youtube_analyzer"]
)

def get_youtube_service():
    """Инициализирует и возвращает сервис YouTube API."""
    if not YOUTUBE_API_KEY:
        return None # Возвращаем None, если ключ не установлен
        
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        return youtube
    except Exception as e:
        print(f"Error initializing YouTube service: {e}")
        return None

@router.get("/analyze/{channel_id}", response_model=ChannelAnalysis)
def analyze_channel(channel_id: str):
    youtube = get_youtube_service()

    if not youtube:
        # Заглушка для случая, когда API ключ не установлен
        return ChannelAnalysis(
            channel_id=channel_id,
            channel_title="Mock Channel Title",
            subscriber_count=100000,
            video_count=500,
            view_count=50000000,
            status="success (mock data)"
        )

    try:
        # 1. Получение информации о канале
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

        if not response.get('items'):
            raise HTTPException(status_code=404, detail=f"Channel with ID {channel_id} not found.")

        channel_data = response['items'][0]
        statistics = channel_data['statistics']

        # 2. Формирование ответа
        analysis = ChannelAnalysis(
            channel_id=channel_id,
            channel_title=channel_data['snippet']['title'],
            subscriber_count=int(statistics.get('subscriberCount', 0)),
            video_count=int(statistics.get('videoCount', 0)),
            view_count=int(statistics.get('viewCount', 0)),
            status="success (live data)"
        )
        return analysis

    except Exception as e:
        print(f"YouTube API Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze channel: {e}")
