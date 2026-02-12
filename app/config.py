from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""

    PROJECT_NAME: str = "FastAPI Enterprise Demo"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"

    # CORS配置
    ALLOWED_HOSTS: List[str] = ["*"]

    # 日志配置
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
