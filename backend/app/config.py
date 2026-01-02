from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
 # Database
 database_url: str 

 # Hugging Face
 HUGGINGFACE_API_KEY: str
 HUGGINGFACE_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.1"

 # CORS
 CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

 # APP
 APP_NAME: str = "AI Blog Generator API"
 APP_VERSION: str = "1.0.0"
 APP_ENVIRONMENT: str = "development"

 @property
 def cors_origins_list(self) -> List[str]:
     return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
 
 # Modern Pydantic Settings Config
 model_config = SettingsConfigDict(
    env_file=".env", 
    env_file_encoding="utf-8",
    case_sensitive=True,
    extra="ignore"
    )
 
 settings = Settings()