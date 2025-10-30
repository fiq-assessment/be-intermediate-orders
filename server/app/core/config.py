from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017/?replicaSet=rs0"
    DB_NAME: str = "interview_db"
    PORT: int = 4000
    ENV: str = "dev"

    class Config:
        env_file = ".env"

settings = Settings()

