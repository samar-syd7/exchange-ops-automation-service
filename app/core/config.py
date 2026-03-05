from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    APP_NAME: str = "exchange-ops-automation-service"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    DATABASE_URL: str 
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str 
    
    ENABLE_SCHEDULER: bool = True
    
    RECONCILIATION_INTERVAL_SECONDS: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()