from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 2000
    
    # Yandex GPT (для миграции)
    YANDEX_GPT_API_KEY: Optional[str] = None
    YANDEX_GPT_FOLDER_ID: Optional[str] = None
    YANDEX_GPT_MODEL: str = "yandexgpt-lite"
    YANDEX_GPT_URI: Optional[str] = None
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "info"
    API_VERSION: str = "v1"
    
    # Feature Flags для миграции
    ENABLE_AB_TESTING: bool = False
    YANDEX_GPT_RATIO: float = 0.0
    ENABLE_YANDEX_GPT: bool = False
    FALLBACK_TO_OPENAI: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()