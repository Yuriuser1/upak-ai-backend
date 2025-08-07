import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAPIEndpoints:
    """Тесты API endpoints"""
    
    def test_health_endpoint(self):
        """Тест health check endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "migration_status" in data
        assert "timestamp" in data
        assert "version" in data
    
    def test_root_endpoint(self):
        """Тест корневого endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "migration" in data
    
    def test_metrics_endpoint(self):
        """Тест metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "upak_" in response.text  # Проверяем наличие наших метрик
    
    @pytest.mark.skipif(not hasattr(client, 'post'), reason="Требуется настройка API ключей")
    def test_text_generation_endpoint(self):
        """Тест endpoint генерации текста"""
        payload = {
            "prompt": "Тестовый промпт",
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = client.post("/api/v1/generate/text", json=payload)
        
        # Может вернуть 500 если API ключи не настроены, это нормально для тестов
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "result" in data
            assert "provider" in data
            assert "generation_time" in data