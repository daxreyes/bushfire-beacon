import sys
import secrets
from typing import List, Union
from loguru import logger
from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"

    PROJECT_NAME: str = "Bushfire Beacon"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5000",
        "http://localhost:8080",
        "http://localhost:8100",
    ]

    BROADCAST_URL: str = "memory://"

    MESSAGE_STREAM_DELAY: float = 1

    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./busfire.db"
    # SQLALCHEMY_DATABASE_URL: str = "postgresql://user:password@postgresserver/db"

    EMAILS_FROM_NAME: str = "Cobeds 19"
    EMAILS_FROM_EMAIL: str = ""  # noreply@example.com

    SMTP_HOST: str = None
    SMTP_PORT: int = None
    SMTP_TLS: bool = True
    SMTP_USER: str = "cobeds19@datascience.group"
    SMTP_PASSWORD: str = ""

    EMAIL_TEMPLATES_DIR: str = "templates"
    EMAILS_ENABLED: bool = False
    ACCOUNT_VERIFY_EXPIRE_HOURS: int = 1
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 1

    SERVER_HOST: str = "https://datascience.group/cobeds19"

    USERS_OPEN_REGISTRATION: bool = True

    LOG_LEVEL: str = "INFO"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

logger.remove()
logger.add(sys.stderr, level=settings.LOG_LEVEL)
