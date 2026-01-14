from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()
