import openai
from app.core.config import settings
from app.core.monitoring import AI_GENERATION_COUNT, AI_GENERATION_DURATION, AI_GENERATION_ERRORS
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
    
    async def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Генерация текста через OpenAI API"""
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            generated_text = response.choices[0].message.content
            generation_time = time.time() - start_time
            
            # Метрики
            AI_GENERATION_COUNT.labels(provider="openai", model=self.model).inc()
            AI_GENERATION_DURATION.labels(provider="openai").observe(generation_time)
            
            logger.info(f"OpenAI генерация завершена за {generation_time:.2f}с")
            
            return {
                "text": generated_text,
                "provider": "openai",
                "model": self.model,
                "generation_time": generation_time,
                "tokens_used": response.usage.total_tokens if response.usage else None
            }
            
        except Exception as e:
            AI_GENERATION_ERRORS.labels(provider="openai", error_type=type(e).__name__).inc()
            logger.error(f"Ошибка OpenAI генерации: {e}")
            raise
    
    async def generate_image(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Генерация изображения через DALL-E"""
        start_time = time.time()
        
        try:
            response = self.client.images.generate(
                prompt=prompt,
                n=1,
                size=kwargs.get('size', '1024x1024')
            )
            
            image_url = response.data[0].url
            generation_time = time.time() - start_time
            
            # Метрики
            AI_GENERATION_COUNT.labels(provider="openai", model="dall-e").inc()
            AI_GENERATION_DURATION.labels(provider="openai").observe(generation_time)
            
            logger.info(f"DALL-E генерация завершена за {generation_time:.2f}с")
            
            return {
                "image_url": image_url,
                "provider": "openai",
                "model": "dall-e",
                "generation_time": generation_time
            }
            
        except Exception as e:
            AI_GENERATION_ERRORS.labels(provider="openai", error_type=type(e).__name__).inc()
            logger.error(f"Ошибка DALL-E генерации: {e}")
            raise