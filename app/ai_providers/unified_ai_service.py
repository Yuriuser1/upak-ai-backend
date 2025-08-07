import random
import logging
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.monitoring import AB_TEST_REQUESTS
from app.services.openai_service import OpenAIService
from app.ai_providers.yandex_gpt_wrapper import YandexGPTService

logger = logging.getLogger(__name__)

class UnifiedAIService:
    """Унифицированный сервис для работы с разными AI провайдерами"""
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.yandex_service = YandexGPTService()
    
    def _choose_provider_for_text(self) -> str:
        """Выбор провайдера для генерации текста на основе настроек A/B тестирования"""
        if not settings.ENABLE_AB_TESTING:
            if settings.ENABLE_YANDEX_GPT:
                return "yandex"
            return "openai"
        
        # A/B тестирование
        if random.random() < settings.YANDEX_GPT_RATIO:
            AB_TEST_REQUESTS.labels(provider="yandex").inc()
            return "yandex"
        else:
            AB_TEST_REQUESTS.labels(provider="openai").inc()
            return "openai"
    
    async def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Генерация текста с автоматическим выбором провайдера"""
        provider = self._choose_provider_for_text()
        
        try:
            if provider == "yandex":
                return await self.yandex_service.generate_text(prompt, **kwargs)
            else:
                return await self.openai_service.generate_text(prompt, **kwargs)
                
        except Exception as e:
            logger.error(f"Ошибка генерации текста через {provider}: {e}")
            
            # Fallback логика
            if settings.FALLBACK_TO_OPENAI and provider == "yandex":
                logger.info("Переключение на OpenAI как fallback")
                try:
                    result = await self.openai_service.generate_text(prompt, **kwargs)
                    result["fallback_used"] = True
                    result["original_provider"] = "yandex"
                    return result
                except Exception as fallback_error:
                    logger.error(f"Fallback также не удался: {fallback_error}")
            
            raise
    
    async def generate_image(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Генерация изображений (пока только через OpenAI)"""
        # В ЭТАПЕ 4 добавим поддержку Kandinsky
        return await self.openai_service.generate_image(prompt, **kwargs)