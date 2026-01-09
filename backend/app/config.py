from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/crypto_analytics"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "crypto_analytics"
    db_user: str = "postgres"
    db_password: str = "postgres"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origins: str = "http://localhost:3000"
    
    # API Keys
    coinmarketcap_api_key: str = ""
    coingecko_api_key: str = ""
    binance_ws_url: str = "wss://stream.binance.com:9443/ws"
    
    # App Settings
    app_name: str = "Crypto Analytics API"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
