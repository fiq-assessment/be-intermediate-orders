from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://fiqtestuser:F9dAd0e0w!!%40@mysql1.interview.servers.fulfillmentiq.com:27017/fiqtest?authMechanism=SCRAM-SHA-1&authSource=admin"
    DB_NAME: str = "fiqtest"
    PORT: int = 4000
    ENV: str = "dev"

    class Config:
        env_file = ".env"

settings = Settings()

