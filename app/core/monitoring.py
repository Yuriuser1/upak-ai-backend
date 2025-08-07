from prometheus_client import Counter, Histogram, generate_latest
from fastapi import FastAPI, Response
import time

# Метрики
REQUEST_COUNT = Counter('upak_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('upak_request_duration_seconds', 'Request duration')
AI_GENERATION_COUNT = Counter('upak_ai_generations_total', 'AI generations', ['provider', 'model'])
AI_GENERATION_DURATION = Histogram('upak_ai_generation_duration_seconds', 'AI generation duration', ['provider'])
AI_GENERATION_ERRORS = Counter('upak_ai_generation_errors_total', 'AI generation errors', ['provider', 'error_type'])
AB_TEST_REQUESTS = Counter('upak_ab_test_requests_total', 'A/B test requests', ['provider'])

def setup_monitoring(app: FastAPI):
    @app.middleware("http")
    async def add_process_time_header(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.observe(process_time)
        return response
    
    @app.get("/metrics")
    async def metrics():
        return Response(generate_latest(), media_type="text/plain")