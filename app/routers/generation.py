from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ai_providers.unified_ai_service import UnifiedAIService
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/generate", tags=["generation"])

class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 2000
    temperature: Optional[float] = 0.7

class ImageGenerationRequest(BaseModel):
    prompt: str
    size: Optional[str] = "1024x1024"

class GenerationResponse(BaseModel):
    result: str
    provider: str
    model: str
    generation_time: float
    tokens_used: Optional[int] = None
    fallback_used: Optional[bool] = False
    original_provider: Optional[str] = None

@router.post("/text", response_model=GenerationResponse)
async def generate_text(request: TextGenerationRequest):
    """Генерация текста через унифицированный AI сервис"""
    try:
        ai_service = UnifiedAIService()
        result = await ai_service.generate_text(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return GenerationResponse(
            result=result["text"],
            provider=result["provider"],
            model=result["model"],
            generation_time=result["generation_time"],
            tokens_used=result.get("tokens_used"),
            fallback_used=result.get("fallback_used", False),
            original_provider=result.get("original_provider")
        )
    
    except Exception as e:
        logger.error(f"Ошибка генерации текста: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/image", response_model=GenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """Генерация изображения"""
    try:
        ai_service = UnifiedAIService()
        result = await ai_service.generate_image(
            prompt=request.prompt,
            size=request.size
        )
        
        return GenerationResponse(
            result=result["image_url"],
            provider=result["provider"],
            model=result["model"],
            generation_time=result["generation_time"]
        )
    
    except Exception as e:
        logger.error(f"Ошибка генерации изображения: {e}")
        raise HTTPException(status_code=500, detail=str(e))