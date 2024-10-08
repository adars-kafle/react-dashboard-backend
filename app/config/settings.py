from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DOMAIN: str
    ENVIRONMENT: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"


settings_config = Settings()
