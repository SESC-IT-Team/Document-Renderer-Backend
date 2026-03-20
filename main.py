import asyncio

from src.config import Settings
from src.utils.S3Storage import S3Storage


async def main():
    settings = Settings()

    endpoint_url = f"http://{settings.S3_URL}:{settings.S3_PORT}"

    storage = S3Storage(
        endpoint_url=endpoint_url,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        bucket_name="your-bucket-name",
    )

    await storage.connect()
    await storage.upload_file("certificate.pdf", "certificate.pdf")


if __name__ == "__main__":
    asyncio.run(main())
