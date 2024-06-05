from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env", extra="allow")

    LOG_PATH: str
    LOG_ROTATION: str = "1 day"
    LOG_LEVEL: str = "INFO"
    LOG_COMPRESSION: str = "zip"
    ENABLE_LOGGING_FILE: bool = True

    FASTAPI_PORT: int

    API_URL: str = "/api/v1"
    API_NAME: str = "fastapi-redis-demo"

    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_PASSWORD: str


settings = Settings()
