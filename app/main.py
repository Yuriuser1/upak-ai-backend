from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import generation, health
from app.core.config import settings
from app.core.monitoring import setup_monitoring
import logging

# Настройка логирования
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="UPAK AI Backend",
    description="Система генерации контента с использованием ИИ (OpenAI → Yandex GPT миграция)",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Мониторинг
setup_monitoring(app)

# Роутеры
app.include_router(generation.router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(health.router, prefix=f"/api/{settings.API_VERSION}")

@app.on_event("startup")
async def startup_event():
    logger.info("UPAK AI Backend запущен")
    logger.info(f"A/B тестирование: {'включено' if settings.ENABLE_AB_TESTING else 'выключено'}")
    logger.info(f"Yandex GPT ratio: {settings.YANDEX_GPT_RATIO}")
    logger.info(f"Fallback на OpenAI: {'включен' if settings.FALLBACK_TO_OPENAI else 'выключен'}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("UPAK AI Backend остановлен")

@app.get("/")
async def root():
    return {
        "message": "UPAK AI Backend",
        "status": "running",
        "migration": "OpenAI → Yandex GPT",
        "docs": "/docs"
    }