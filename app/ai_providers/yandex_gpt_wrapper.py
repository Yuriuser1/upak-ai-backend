import aiohttp
import json
import time
import logging
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.monitoring import AI_GENERATION_COUNT, AI_GENERATION_DURATION, AI_GENERATION_ERRORS

logger = logging.getLogger(__name__)

class YandexGPTService:
    """Wrapper для Yandex GPT API с унифицированным интерфейсом"""
    
    def __init__(self):
        self.api_key = settings.YANDEX_GPT_API_KEY
        self.folder_id = settings.YANDEX_GPT_FOLDER_ID
        self.model = settings.YANDEX_GPT_MODEL
        self.uri = settings.YANDEX_GPT_URI or f"gpt://{self.folder_id}/{self.model}"
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1"
        
        if not self.api_key or not self.folder_id:
            logger.warning("Yandex GPT credentials не настроены")
    
    async def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Генерация текста через Yandex GPT API"""
        start_time = time.time()
        
        if not self.api_key or not self.folder_id:
            raise ValueError("Yandex GPT credentials не настроены")
        
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "modelUri": self.uri,
            "completionOptions": {
                "stream": False,
                "temperature": kwargs.get('temperature', 0.7),
                "maxTokens": str(kwargs.get('max_tokens', 2000))
            },
            "messages": [
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/completion",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Yandex GPT API error {response.status}: {error_text}")
                    
                    result = await response.json()
                    
            generated_text = result["result"]["alternatives"][0]["message"]["text"]
            generation_time = time.time() - start_time
            
            # Метрики
            AI_GENERATION_COUNT.labels(provider="yandex", model=self.model).inc()
            AI_GENERATION_DURATION.labels(provider="yandex").observe(generation_time)
            
            logger.info(f"Yandex GPT генерация завершена за {generation_time:.2f}с")
            
            return {
                "text": generated_text,
                "provider": "yandex",
                "model": self.model,
                "generation_time": generation_time,
                "tokens_used": result["result"]["usage"].get("totalTokens") if "usage" in result["result"] else None
            }
            
        except Exception as e:
            AI_GENERATION_ERRORS.labels(provider="yandex", error_type=type(e).__name__).inc()
            logger.error(f"Ошибка Yandex GPT генерации: {e}")
            raise
    
    async def generate_image(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Заглушка для генерации изображений (будет реализована в ЭТАПЕ 4)"""
        raise NotImplementedError("Генерация изображений через Yandex пока не реализована. Используйте OpenAI DALL-E.")