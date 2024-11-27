from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    gmail_client_id: str
    gmail_client_secret: str
    gemini_api_key: str
    openai_api_key: str
    frontend_base_url: str

    class Config:
        env_file = ".env"

settings = Settings()