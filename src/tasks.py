from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from src.config import Settings
from src.core.renderer import Renderer

settings = Settings()

broker = AioPikaBroker(
    url=settings.TASKIQ_BROKER_URL,
).with_result_backend(
    RedisAsyncResultBackend(
        redis_url=settings.TASKIQ_BACKEND_URL,
    ),
)


@broker.task
async def generate_certificate_task(
    template_content: str,
    data: dict,
    filename: str | None = None,
    bucket_name: str | None = None,
) -> dict:
    try:
        bucket_name = bucket_name or settings.BUCKET_NAME
        file_url = await Renderer.render(
            template=template_content,
            data=data,
            filename=filename,
            bucket_name=bucket_name,
        )
        return {"status": "success", "file_url": file_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}
