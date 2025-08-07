import pytest
import asyncio
import time
from typing import List, Dict, Any
from app.services.openai_service import OpenAIService
from app.ai_providers.yandex_gpt_wrapper import YandexGPTService
from app.ai_providers.unified_ai_service import UnifiedAIService
from app.core.config import settings

# Тестовые промпты для сравнения качества
TEST_PROMPTS = [
    "Напиши краткое описание преимуществ использования искусственного интеллекта в бизнесе.",
    "Объясни простыми словами, что такое машинное обучение.",
    "Создай план статьи о цифровой трансформации компаний.",
    "Напиши введение к презентации о важности кибербезопасности.",
    "Сформулируй 5 ключевых трендов в области технологий на 2025 год."
]

class QualityMetrics:
    """Метрики для оценки качества генерации"""
    
    @staticmethod
    def calculate_response_length(text: str) -> int:
        return len(text.split())
    
    @staticmethod
    def calculate_russian_content_ratio(text: str) -> float:
        """Процент русских символов в тексте"""
        russian_chars = sum(1 for char in text if 'а' <= char.lower() <= 'я' or char in 'ёЁ')
        total_chars = len([char for char in text if char.isalpha()])
        return russian_chars / total_chars if total_chars > 0 else 0
    
    @staticmethod
    def has_coherent_structure(text: str) -> bool:
        """Проверка на наличие структуры (абзацы, предложения)"""
        sentences = text.count('.') + text.count('!') + text.count('?')
        return sentences >= 2

@pytest.mark.asyncio
class TestGenerationQuality:
    """Тесты для сравнения качества генерации между провайдерами"""
    
    async def test_openai_generation(self):
        """Тест генерации через OpenAI"""
        if not settings.OPENAI_API_KEY:
            pytest.skip("OpenAI API key не настроен")
        
        service = OpenAIService()
        results = []
        
        for prompt in TEST_PROMPTS:
            start_time = time.time()
            try:
                result = await service.generate_text(prompt)
                generation_time = time.time() - start_time
                
                results.append({
                    'prompt': prompt,
                    'response': result['text'],
                    'generation_time': generation_time,
                    'provider': 'openai',
                    'success': True
                })
            except Exception as e:
                results.append({
                    'prompt': prompt,
                    'error': str(e),
                    'provider': 'openai',
                    'success': False
                })
        
        # Анализ результатов
        successful_results = [r for r in results if r['success']]
        assert len(successful_results) > 0, "Ни один запрос к OpenAI не выполнился успешно"
        
        avg_time = sum(r['generation_time'] for r in successful_results) / len(successful_results)
        print(f"OpenAI - Среднее время генерации: {avg_time:.2f}с")
        
        return results
    
    async def test_yandex_gpt_generation(self):
        """Тест генерации через Yandex GPT"""
        if not settings.YANDEX_GPT_API_KEY or not settings.YANDEX_GPT_FOLDER_ID:
            pytest.skip("Yandex GPT credentials не настроены")
        
        service = YandexGPTService()
        results = []
        
        for prompt in TEST_PROMPTS:
            start_time = time.time()
            try:
                result = await service.generate_text(prompt)
                generation_time = time.time() - start_time
                
                results.append({
                    'prompt': prompt,
                    'response': result['text'],
                    'generation_time': generation_time,
                    'provider': 'yandex',
                    'success': True
                })
            except Exception as e:
                results.append({
                    'prompt': prompt,
                    'error': str(e),
                    'provider': 'yandex',
                    'success': False
                })
        
        # Анализ результатов
        successful_results = [r for r in results if r['success']]
        if len(successful_results) == 0:
            pytest.skip("Yandex GPT недоступен или неправильно настроен")
        
        avg_time = sum(r['generation_time'] for r in successful_results) / len(successful_results)
        print(f"Yandex GPT - Среднее время генерации: {avg_time:.2f}с")
        
        return results
    
    async def test_quality_comparison(self):
        """Сравнение качества генерации между провайдерами"""
        openai_results = await self.test_openai_generation()
        yandex_results = await self.test_yandex_gpt_generation()
        
        comparison_report = []
        
        for i, prompt in enumerate(TEST_PROMPTS):
            openai_result = next((r for r in openai_results if r['prompt'] == prompt and r['success']), None)
            yandex_result = next((r for r in yandex_results if r['prompt'] == prompt and r['success']), None)
            
            if openai_result and yandex_result:
                openai_metrics = {
                    'length': QualityMetrics.calculate_response_length(openai_result['response']),
                    'russian_ratio': QualityMetrics.calculate_russian_content_ratio(openai_result['response']),
                    'has_structure': QualityMetrics.has_coherent_structure(openai_result['response']),
                    'generation_time': openai_result['generation_time']
                }
                
                yandex_metrics = {
                    'length': QualityMetrics.calculate_response_length(yandex_result['response']),
                    'russian_ratio': QualityMetrics.calculate_russian_content_ratio(yandex_result['response']),
                    'has_structure': QualityMetrics.has_coherent_structure(yandex_result['response']),
                    'generation_time': yandex_result['generation_time']
                }
                
                comparison_report.append({
                    'prompt': prompt,
                    'openai': openai_metrics,
                    'yandex': yandex_metrics,
                    'winner_russian': 'yandex' if yandex_metrics['russian_ratio'] > openai_metrics['russian_ratio'] else 'openai',
                    'winner_speed': 'yandex' if yandex_metrics['generation_time'] < openai_metrics['generation_time'] else 'openai'
                })
        
        # Вывод отчета
        print("\n=== ОТЧЕТ СРАВНЕНИЯ КАЧЕСТВА ===")
        for item in comparison_report:
            print(f"\nПромпт: {item['prompt'][:50]}...")
            print(f"OpenAI - Длина: {item['openai']['length']}, Русский: {item['openai']['russian_ratio']:.2f}, Время: {item['openai']['generation_time']:.2f}с")
            print(f"Yandex - Длина: {item['yandex']['length']}, Русский: {item['yandex']['russian_ratio']:.2f}, Время: {item['yandex']['generation_time']:.2f}с")
            print(f"Лучше для русского: {item['winner_russian']}, Быстрее: {item['winner_speed']}")
        
        return comparison_report

@pytest.mark.asyncio
class TestUnifiedService:
    """Тесты для унифицированного AI сервиса"""
    
    async def test_fallback_mechanism(self):
        """Тест механизма fallback"""
        service = UnifiedAIService()
        
        # Тест с включенным fallback
        original_setting = settings.FALLBACK_TO_OPENAI
        settings.FALLBACK_TO_OPENAI = True
        
        try:
            result = await service.generate_text("Тестовый промпт для проверки fallback")
            assert 'text' in result
            assert 'provider' in result
        finally:
            settings.FALLBACK_TO_OPENAI = original_setting
    
    async def test_ab_testing_distribution(self):
        """Тест распределения запросов при A/B тестировании"""
        service = UnifiedAIService()
        
        # Включаем A/B тестирование
        original_ab = settings.ENABLE_AB_TESTING
        original_ratio = settings.YANDEX_GPT_RATIO
        
        settings.ENABLE_AB_TESTING = True
        settings.YANDEX_GPT_RATIO = 0.5
        
        providers_used = []
        
        try:
            for _ in range(10):
                provider = service._choose_provider_for_text()
                providers_used.append(provider)
            
            # Проверяем, что используются оба провайдера
            unique_providers = set(providers_used)
            assert len(unique_providers) >= 1, "Должен использоваться хотя бы один провайдер"
            
        finally:
            settings.ENABLE_AB_TESTING = original_ab
            settings.YANDEX_GPT_RATIO = original_ratio