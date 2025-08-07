# UPAK AI Backend API Documentation

## Обзор

UPAK AI Backend предоставляет унифицированный API для генерации контента с использованием различных ИИ провайдеров (OpenAI, Yandex GPT).

**Base URL**: `http://localhost:8000/api/v1`

## Аутентификация

В текущей версии аутентификация не требуется. В продакшене рекомендуется добавить API ключи.

## Endpoints

### Генерация текста

**POST** `/generate/text`

Генерирует текст на основе промпта с автоматическим выбором оптимального ИИ провайдера.

#### Request Body
```json
{
  "prompt": "Напиши краткое описание преимуществ ИИ в бизнесе",
  "max_tokens": 2000,
  "temperature": 0.7
}
```

#### Parameters
- `prompt` (string, required): Текст промпта для генерации
- `max_tokens` (integer, optional): Максимальное количество токенов (по умолчанию: 2000)
- `temperature` (float, optional): Температура генерации 0.0-1.0 (по умолчанию: 0.7)

#### Response
```json
{
  "result": "Искусственный интеллект предоставляет бизнесу множество преимуществ...",
  "provider": "yandex",
  "model": "yandexgpt-lite",
  "generation_time": 1.23,
  "tokens_used": 150,
  "fallback_used": false,
  "original_provider": null
}
```

#### Response Fields
- `result`: Сгенерированный текст
- `provider`: Использованный провайдер ("openai" или "yandex")
- `model`: Модель ИИ
- `generation_time`: Время генерации в секундах
- `tokens_used`: Количество использованных токенов
- `fallback_used`: Был ли использован fallback механизм
- `original_provider`: Изначально выбранный провайдер (если был fallback)

### Генерация изображений

**POST** `/generate/image`

Генерирует изображение на основе текстового описания.

#### Request Body
```json
{
  "prompt": "Красивый закат над морем в стиле импрессионизма",
  "size": "1024x1024"
}
```

#### Parameters
- `prompt` (string, required): Описание изображения
- `size` (string, optional): Размер изображения (по умолчанию: "1024x1024")

#### Response
```json
{
  "result": "https://example.com/generated-image.png",
  "provider": "openai",
  "model": "dall-e",
  "generation_time": 5.67
}
```

### Проверка состояния

**GET** `/health`

Возвращает информацию о состоянии системы и статусе миграции.

#### Response
```json
{
  "status": "healthy",
  "timestamp": 1691234567.89,
  "version": "1.0.0",
  "config": {
    "openai_model": "gpt-4",
    "yandex_gpt_model": "yandexgpt-lite",
    "debug": true
  },
  "migration_status": {
    "ab_testing_enabled": true,
    "yandex_gpt_ratio": 0.5,
    "yandex_gpt_enabled": true,
    "fallback_to_openai": true,
    "yandex_credentials_configured": true
  }
}
```

### Метрики

**GET** `/metrics`

Возвращает метрики Prometheus для мониторинга.

#### Response
```
# HELP upak_ai_generations_total AI generations
# TYPE upak_ai_generations_total counter
upak_ai_generations_total{provider="openai",model="gpt-4"} 42.0
upak_ai_generations_total{provider="yandex",model="yandexgpt-lite"} 38.0
...
```

## Коды ошибок

- `200 OK`: Успешный запрос
- `400 Bad Request`: Неверные параметры запроса
- `500 Internal Server Error`: Внутренняя ошибка сервера
- `503 Service Unavailable`: Сервис временно недоступен

## Примеры использования

### Python
```python
import requests

# Генерация текста
response = requests.post(
    "http://localhost:8000/api/v1/generate/text",
    json={
        "prompt": "Объясни квантовые вычисления простыми словами",
        "max_tokens": 500,
        "temperature": 0.8
    }
)

result = response.json()
print(f"Провайдер: {result['provider']}")
print(f"Текст: {result['result']}")
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/api/v1/generate/text', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: 'Создай план маркетинговой кампании для стартапа',
    max_tokens: 1000,
    temperature: 0.7
  })
});

const result = await response.json();
console.log('Результат:', result.result);
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/generate/text" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Напиши краткий обзор трендов ИИ в 2025 году",
    "max_tokens": 800,
    "temperature": 0.6
  }'
```

## Особенности миграции

### A/B тестирование

Во время миграции система автоматически распределяет запросы между OpenAI и Yandex GPT согласно настроенному соотношению.

### Fallback механизм

Если Yandex GPT недоступен, система автоматически переключается на OpenAI (при включенном fallback).

### Мониторинг

Все запросы логируются и отслеживаются через метрики Prometheus. Доступны дашборды в Grafana для визуализации.

## Swagger UI

Интерактивная документация API доступна по адресу: `http://localhost:8000/docs`

---

*Документация обновлена: 7 августа 2025*