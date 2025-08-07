from fastapi import APIRouter
from pydantic import BaseModel
from app.core.config import settings
import time

router = APIRouter(tags=["health"])

class HealthResponse(BaseModel):
    status: str
    timestamp: float
    version: str
    config: dict
    migration_status: dict

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка состояния системы с информацией о миграции"""
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        version="1.0.0",
        config={
            "openai_model": settings.OPENAI_MODEL,
            "yandex_gpt_model": settings.YANDEX_GPT_MODEL,
            "debug": settings.DEBUG,
        },
        migration_status={
            "ab_testing_enabled": settings.ENABLE_AB_TESTING,
            "yandex_gpt_ratio": settings.YANDEX_GPT_RATIO,
            "yandex_gpt_enabled": settings.ENABLE_YANDEX_GPT,
            "fallback_to_openai": settings.FALLBACK_TO_OPENAI,
            "yandex_credentials_configured": bool(settings.YANDEX_GPT_API_KEY and settings.YANDEX_GPT_FOLDER_ID)
        }
    )