from pydantic_settings import BaseSettings
from urllib.parse import quote


password = quote("zaq12WSX")
encode_password = quote(password)


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI"
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://postgres:{password}@database:5432/postgres_services"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    JWT_SECRET_KEY: str ="b2c2e4e8c0e8e0e8e4e2c2b2"
    JWT_ALGORITHM: str = "HS256"
    class Config:
        env_file = ".env"


settings = Settings()
