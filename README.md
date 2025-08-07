# 🚀 UPAK AI Backend - Миграция на Yandex GPT

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/Yuriuser1/upak-ai-backend)
[![Migration Status](https://img.shields.io/badge/migration-ready-blue)](https://github.com/Yuriuser1/upak-ai-backend/pull/1)
[![API Version](https://img.shields.io/badge/api-v1-orange)](http://localhost:8000/docs)

Система генерации контента с использованием ИИ для платформы UPAK с поддержкой миграции с OpenAI на Yandex GPT.

## 🎯 Цели миграции

- **💰 Экономия**: Снижение затрат на 30-35%
- **🇷🇺 Качество**: Улучшение русскоязычного контента
- **🛡️ Независимость**: Снижение зависимости от зарубежных сервисов
- **📈 Масштабируемость**: Готовность к росту

## ⚡ Быстрый старт

### 1. Клонирование и настройка
```bash
git clone https://github.com/Yuriuser1/upak-ai-backend.git
cd upak-ai-backend
git checkout feature/yandex-gpt-migration

# Автоматическая настройка
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh
```

### 2. Настройка API ключей
```bash
# Скопируйте и отредактируйте .env файл
cp config/example.env .env
nano .env

# Обязательные переменные:
# OPENAI_API_KEY=sk-...
# YANDEX_GPT_API_KEY=AQVNxxxxxxxx
# YANDEX_GPT_FOLDER_ID=b1gxxxxxxxx
```

### 3. Запуск системы
```bash
# Локальная разработка
source venv/bin/activate
python -m uvicorn app.main:app --reload

# Или через Docker
docker-compose up -d
```

### 4. Проверка работы
- **API документация**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/api/v1/health
- **Grafana мониторинг**: http://localhost:3000 (admin/admin)
- **Prometheus метрики**: http://localhost:9090

## 🔄 Управление миграцией

### Проверка текущего статуса
```bash
python scripts/migration_control.py --status
```

### Этапы миграции
```bash
# ЭТАП 1: A/B тестирование 50/50
python scripts/migration_control.py --stage 1

# ЭТАП 2: Увеличение доли Yandex GPT до 75%
python scripts/migration_control.py --stage 2

# ЭТАП 3: Полная миграция на Yandex GPT
python scripts/migration_control.py --stage 3

# Откат к OpenAI (в случае проблем)
python scripts/migration_control.py --rollback
```

## 📊 API Endpoints

### Генерация текста
```bash
curl -X POST "http://localhost:8000/api/v1/generate/text" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Напиши краткое описание преимуществ ИИ в бизнесе",
    "max_tokens": 1000,
    "temperature": 0.7
  }'
```

### Генерация изображений
```bash
curl -X POST "http://localhost:8000/api/v1/generate/image" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Красивый закат над морем",
    "size": "1024x1024"
  }'
```

### Проверка состояния
```bash
curl http://localhost:8000/api/v1/health
```

## 🏗️ Архитектура

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│  UPAK Backend    │───▶│  AI Providers   │
│                 │    │                  │    │                 │
│ - Web App       │    │ - FastAPI        │    │ - OpenAI GPT    │
│ - Mobile App    │    │ - UnifiedAI      │    │ - Yandex GPT    │
│ - API Clients   │    │ - A/B Testing    │    │ - DALL-E        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌────────▼────────┐
                       │   Monitoring    │
                       │                 │
                       │ - Prometheus    │
                       │ - Grafana       │
                       │ - Metrics       │
                       └─────────────────┘
```

## 🧪 Тестирование

### Автоматические тесты
```bash
# Все тесты
pytest

# Тесты качества генерации
pytest tests/test_generation_quality.py -v

# API тесты
pytest tests/test_api_endpoints.py -v

# Тесты с покрытием
pytest --cov=app tests/
```

### Нагрузочное тестирование
```bash
pip install locust
locust -f tests/load_test.py --host=http://localhost:8000
```

## 📈 Мониторинг

### Ключевые метрики
- `upak_ai_generations_total` - Количество генераций по провайдерам
- `upak_ai_generation_duration_seconds` - Время генерации
- `upak_ai_generation_errors_total` - Ошибки по провайдерам
- `upak_ab_test_requests_total` - Распределение A/B тестов

### Grafana дашборды
1. **AI Performance**: Производительность генерации
2. **A/B Testing**: Распределение между провайдерами
3. **Error Monitoring**: Отслеживание ошибок
4. **Cost Analysis**: Анализ затрат

## 🚀 Развертывание

### Docker Compose (рекомендуется)
```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f upak-backend

# Остановка
docker-compose down
```

### Kubernetes
```bash
# Создание namespace
kubectl create namespace upak-ai

# Создание секретов
kubectl create secret generic upak-secrets \
  --from-literal=openai-api-key="your_key" \
  --from-literal=yandex-gpt-api-key="your_key" \
  --from-literal=yandex-gpt-folder-id="your_id" \
  -n upak-ai

# Развертывание
kubectl apply -f k8s/ -n upak-ai
```

## 🔒 Безопасность

### Рекомендации для продакшена
1. **API ключи**: Используйте секреты Kubernetes/Docker
2. **HTTPS**: Настройте SSL/TLS сертификаты
3. **Аутентификация**: Добавьте API ключи или JWT
4. **Мониторинг**: Настройте алерты на подозрительную активность

### Резервное копирование
```bash
# Автоматический backup конфигурации
python scripts/migration_control.py --backup

# Восстановление
python scripts/migration_control.py --restore backup_20250807_120000.env
```

## 📚 Документация

- [📋 План миграции](docs/migration_plan.md) - Подробный план всех этапов
- [🔧 API документация](docs/api_documentation.md) - Полное описание API
- [🚀 Руководство по развертыванию](docs/deployment_guide.md) - Инструкции по установке
- [🎨 Исследование Kandinsky](docs/kandinsky_evaluation.md) - Альтернативы для изображений

## 🔧 Конфигурация

### Основные переменные
```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Yandex GPT
YANDEX_GPT_API_KEY=AQVNxxxxxxxx
YANDEX_GPT_FOLDER_ID=b1gxxxxxxxx
YANDEX_GPT_MODEL=yandexgpt-lite

# Управление миграцией
ENABLE_AB_TESTING=false
YANDEX_GPT_RATIO=0.0
ENABLE_YANDEX_GPT=false
FALLBACK_TO_OPENAI=true
```

## 🐛 Устранение неполадок

### Частые проблемы

#### API ключи не работают
```bash
# Проверка OpenAI
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Проверка Yandex GPT
curl -H "Authorization: Api-Key $YANDEX_GPT_API_KEY" \
  https://llm.api.cloud.yandex.net/foundationModels/v1/models
```

#### Проблемы с Docker
```bash
# Пересборка контейнеров
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### Проблемы с миграцией
```bash
# Проверка статуса
python scripts/migration_control.py --status

# Откат к стабильной конфигурации
python scripts/migration_control.py --rollback
```

## 📞 Поддержка

- **🐛 Issues**: [GitHub Issues](https://github.com/Yuriuser1/upak-ai-backend/issues)
- **📖 Wiki**: [Документация](https://github.com/Yuriuser1/upak-ai-backend/wiki)
- **💬 Discussions**: [GitHub Discussions](https://github.com/Yuriuser1/upak-ai-backend/discussions)

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature ветку (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🏆 Статус миграции

| Этап | Статус | Описание |
|------|--------|----------|
| ЭТАП 1 | ✅ Завершен | Подготовительный этап |
| ЭТАП 2 | ✅ Готов | Пилотное внедрение |
| ЭТАП 3 | ✅ Готов | Постепенная миграция |
| ЭТАП 4 | ✅ Готов | Финальная унификация |

---

**🎉 Миграция готова к развертыванию!**

*Последнее обновление: 7 августа 2025*