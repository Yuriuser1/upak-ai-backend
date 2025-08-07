#!/bin/bash

# Скрипт для настройки окружения UPAK AI Backend

set -e

echo "🚀 Настройка окружения UPAK AI Backend"
echo "======================================"

# Проверка Python версии
echo "📋 Проверка Python версии..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Требуется Python $required_version или выше. Текущая версия: $python_version"
    exit 1
fi
echo "✅ Python версия: $python_version"

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
else
    echo "ℹ️  Виртуальное окружение уже существует"
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Обновление pip
echo "⬆️  Обновление pip..."
pip install --upgrade pip

# Установка зависимостей
echo "📚 Установка зависимостей..."
pip install -r requirements.txt

# Создание .env файла из примера
echo "⚙️  Настройка конфигурации..."
if [ ! -f ".env" ]; then
    cp config/example.env .env
    echo "✅ Создан файл .env из примера"
    echo "⚠️  ВАЖНО: Настройте API ключи в файле .env"
else
    echo "ℹ️  Файл .env уже существует"
fi

# Создание директорий
echo "📁 Создание необходимых директорий..."
mkdir -p logs
mkdir -p data
echo "✅ Директории созданы"

# Проверка Docker (опционально)
echo "🐳 Проверка Docker..."
if command -v docker &> /dev/null; then
    echo "✅ Docker установлен: $(docker --version)"
    if command -v docker-compose &> /dev/null; then
        echo "✅ Docker Compose установлен: $(docker-compose --version)"
    else
        echo "⚠️  Docker Compose не найден. Установите для полной функциональности."
    fi
else
    echo "⚠️  Docker не найден. Установите для контейнеризации."
fi

echo ""
echo "🎉 Настройка окружения завершена!"
echo ""
echo "📝 Следующие шаги:"
echo "1. Настройте API ключи в файле .env"
echo "2. Запустите приложение: python -m uvicorn app.main:app --reload"
echo "3. Или используйте Docker: docker-compose up -d"
echo "4. Откройте http://localhost:8000/docs для Swagger UI"
echo ""
echo "🔧 Управление миграцией:"
echo "   python scripts/migration_control.py --status"
echo "   python scripts/migration_control.py --stage 1"
echo ""
echo "📊 Мониторинг:"
echo "   Grafana: http://localhost:3000 (admin/admin)"
echo "   Prometheus: http://localhost:9090"
echo "   Метрики: http://localhost:8000/metrics"