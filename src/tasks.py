import os

from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from src.core.renderer import Renderer
from src.config import Settings

settings = Settings()

broker_url = settings.TASKIQ_BROKER_URL or "amqp://guest:guest@rabbitmq:5672"
backend_url = settings.TASKIQ_BACKEND_URL or "redis://redis:6379"

broker = AioPikaBroker(url=broker_url).with_result_backend(
    RedisAsyncResultBackend(redis_url=backend_url),
)


@broker.task
async def heartbeat_task() -> None:
    print("TaskIQ worker is running")


@broker.task
async def generate_certificate_task(
    template_content: str,
    data: dict,
    filename: str | None = None,
):
    try:
        result_filename = Renderer.render(template_content, data, filename)
        return {"status": "success", "filename": result_filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}
