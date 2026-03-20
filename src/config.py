from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # MinIO
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    S3_URL: str
    S3_PORT: int


    TASKIQ_BROKER_URL: str  # amqp://guest:guest@rabbitmq:5672
    TASKIQ_BACKEND_URL: str  # redis://:REDIS_PASSWORD@redis:6379/0

    REDIS_PASSWORD: str | None = None


settings = Settings()
