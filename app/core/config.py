from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "FastAPI Clean Architecture"
    API_V1_STR: str = "/api/v1"
    MODE: Literal["dev", "prod", "test"] = "dev"
    DATABASE_URL: str

settings = Settings()
