from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    S3_URL: str
    S3_PORT: int
    TASKIQ_BROKER_URL: str
    TASKIQ_BACKEND_URL: str

settings = Settings()
