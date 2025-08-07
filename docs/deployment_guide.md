# Руководство по развертыванию UPAK AI Backend

## Требования к системе

### Минимальные требования
- **CPU**: 2 ядра
- **RAM**: 4 GB
- **Диск**: 20 GB свободного места
- **ОС**: Ubuntu 20.04+ / CentOS 8+ / macOS 10.15+
- **Python**: 3.11+
- **Docker**: 20.10+ (опционально)

### Рекомендуемые требования для продакшена
- **CPU**: 4+ ядра
- **RAM**: 8+ GB
- **Диск**: 100+ GB SSD
- **Сеть**: Стабильное интернет-соединение

## Способы развертывания

### 1. Локальная разработка

#### Быстрый старт
```bash
# Клонирование репозитория
git clone https://github.com/Yuriuser1/upak-ai-backend.git
cd upak-ai-backend

# Переключение на ветку миграции
git checkout feature/yandex-gpt-migration

# Автоматическая настройка окружения
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh

# Настройка API ключей в .env файле
nano .env

# Запуск приложения
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Ручная настройка
```bash
# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Копирование конфигурации
cp config/example.env .env

# Настройка переменных окружения
export OPENAI_API_KEY="your_openai_key"
export YANDEX_GPT_API_KEY="your_yandex_key"
export YANDEX_GPT_FOLDER_ID="your_folder_id"
export DATABASE_URL="postgresql://user:pass@localhost:5432/upak_db"

# Запуск
uvicorn app.main:app --reload
```

### 2. Docker развертывание

#### Простое развертывание
```bash
# Сборка и запуск
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f upak-backend
```

#### Продакшен развертывание
```bash
# Создание продакшен конфигурации
cp docker-compose.yml docker-compose.prod.yml

# Редактирование для продакшена
nano docker-compose.prod.yml

# Запуск в продакшен режиме
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Kubernetes развертывание

#### Создание namespace
```bash
kubectl create namespace upak-ai
```

#### Применение манифестов
```bash
# Secrets для API ключей
kubectl create secret generic upak-secrets \
  --from-literal=openai-api-key="your_openai_key" \
  --from-literal=yandex-gpt-api-key="your_yandex_key" \
  --from-literal=yandex-gpt-folder-id="your_folder_id" \
  -n upak-ai

# Развертывание приложения
kubectl apply -f k8s/ -n upak-ai
```

## Настройка переменных окружения

### Обязательные переменные
```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Yandex GPT
YANDEX_GPT_API_KEY=AQVNxxxxxxxx
YANDEX_GPT_FOLDER_ID=b1gxxxxxxxx
YANDEX_GPT_MODEL=yandexgpt-lite

# База данных
DATABASE_URL=postgresql://user:password@localhost:5432/upak_db
```

### Переменные миграции
```bash
# Управление миграцией
ENABLE_AB_TESTING=false
YANDEX_GPT_RATIO=0.0
ENABLE_YANDEX_GPT=false
FALLBACK_TO_OPENAI=true
```

### Опциональные переменные
```bash
# Приложение
DEBUG=false
LOG_LEVEL=info
API_VERSION=v1

# Redis
REDIS_URL=redis://localhost:6379

# Мониторинг
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
```

## Получение API ключей

### OpenAI API Key
1. Зарегистрируйтесь на [platform.openai.com](https://platform.openai.com)
2. Перейдите в раздел "API Keys"
3. Создайте новый ключ
4. Скопируйте ключ в переменную `OPENAI_API_KEY`

### Yandex GPT API Key
1. Зарегистрируйтесь в [Yandex Cloud](https://cloud.yandex.ru)
2. Создайте сервисный аккаунт
3. Назначьте роль `ai.languageModels.user`
4. Создайте API ключ для сервисного аккаунта
5. Получите Folder ID из консоли Yandex Cloud

## Мониторинг и логирование

### Prometheus метрики
- URL: `http://localhost:9090`
- Метрики: `http://localhost:8000/metrics`

### Grafana дашборды
- URL: `http://localhost:3000`
- Логин: `admin` / Пароль: `admin`
- Импорт дашборда: `monitoring/grafana/dashboards/upak-ai-metrics.json`

### Логи приложения
```bash
# Docker логи
docker-compose logs -f upak-backend

# Локальные логи
tail -f logs/upak-backend.log

# Kubernetes логи
kubectl logs -f deployment/upak-backend -n upak-ai
```

## Управление миграцией

### Проверка статуса
```bash
python scripts/migration_control.py --status
```

### Этапы миграции
```bash
# ЭТАП 1: A/B тестирование 50/50
python scripts/migration_control.py --stage 1

# ЭТАП 2: 75% на Yandex GPT
python scripts/migration_control.py --stage 2

# ЭТАП 3: Полная миграция
python scripts/migration_control.py --stage 3

# Откат к OpenAI
python scripts/migration_control.py --rollback
```

## Тестирование

### Запуск тестов
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
# Установка locust
pip install locust

# Запуск нагрузочного тестирования
locust -f tests/load_test.py --host=http://localhost:8000
```

## Безопасность

### Рекомендации для продакшена
1. **API ключи**: Используйте секреты Kubernetes или Docker secrets
2. **HTTPS**: Настройте SSL/TLS сертификаты
3. **Аутентификация**: Добавьте API ключи или JWT токены
4. **Firewall**: Ограничьте доступ к портам
5. **Мониторинг**: Настройте алерты на подозрительную активность

### Пример nginx конфигурации
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Резервное копирование

### База данных
```bash
# Создание бэкапа
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление
psql $DATABASE_URL < backup_20250807_120000.sql
```

### Конфигурация
```bash
# Автоматический бэкап при изменениях
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
```

## Масштабирование

### Горизонтальное масштабирование
```bash
# Docker Compose
docker-compose up -d --scale upak-backend=3

# Kubernetes
kubectl scale deployment upak-backend --replicas=3 -n upak-ai
```

### Вертикальное масштабирование
```yaml
# docker-compose.yml
services:
  upak-backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

## Устранение неполадок

### Частые проблемы

#### 1. Ошибка подключения к API
```bash
# Проверка API ключей
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Проверка Yandex GPT
curl -H "Authorization: Api-Key $YANDEX_GPT_API_KEY" \
  https://llm.api.cloud.yandex.net/foundationModels/v1/models
```

#### 2. Проблемы с базой данных
```bash
# Проверка подключения
psql $DATABASE_URL -c "SELECT 1;"

# Проверка таблиц
psql $DATABASE_URL -c "\dt"
```

#### 3. Проблемы с Docker
```bash
# Пересборка контейнеров
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Очистка Docker
docker system prune -a
```

### Логи для диагностики
```bash
# Подробные логи приложения
export LOG_LEVEL=debug

# Логи всех компонентов
docker-compose logs --tail=100

# Системные логи
journalctl -u docker -f
```

## Поддержка

- **Документация**: `/docs`
- **API документация**: `http://localhost:8000/docs`
- **Мониторинг**: `http://localhost:3000`
- **Метрики**: `http://localhost:8000/metrics`

---

*Руководство обновлено: 7 августа 2025*