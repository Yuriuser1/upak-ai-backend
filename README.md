# UPAK AI Backend

Система генерации контента с использованием ИИ для платформы UPAK.

## Архитектура

- **Backend**: FastAPI + Python
- **AI Provider**: OpenAI GPT (планируется миграция на Yandex GPT)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Monitoring**: Prometheus + Grafana

## Установка

```bash
pip install -r requirements.txt
cp config/example.env .env
# Настройте переменные окружения
python -m uvicorn app.main:app --reload
```

## API Endpoints

- `POST /api/v1/generate/text` - Генерация текста
- `POST /api/v1/generate/image` - Генерация изображений
- `GET /api/v1/health` - Проверка состояния

## Миграция на Yandex GPT

Текущий статус: **В процессе**
- [x] Создание ветки миграции
- [ ] Адаптация кода для Yandex GPT API
- [ ] A/B тестирование
- [ ] Полная миграция