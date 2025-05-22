from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email Settings
    MAIL_USERNAME: str = "your-email@gmail.com"
    MAIL_PASSWORD: str = "your-app-password"
    MAIL_FROM: str = "your-email@gmail.com"
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    
    class Config:
        env_file = ".env"

settings = Settings()