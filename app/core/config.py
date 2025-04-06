from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    app_name: str = "Vallauri orientamento"
    ssl_enabled: bool = False
    ssl_keyfile: str = ""
    ssl_certfile: str = ""
    DATABASE_URL: str = "sqlite:///./database.db"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30
    VERSION: str = "0.1.0"
    SECRET_KEY: str = "secret"
    SENTRY_RELEASE: str = "0.1.0"
    SENTRY_DSN: str = ""
    MONGODB_CONNECTION_STRING: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "orientati"
    MONGODB_STATS_COLLECTION: str = "stats"
    MONGODB_LOGS_COLLECTION: str = "logs"
    MONGODB_UPDATES_COLLECTION: str = "updates"
    model_config = SettingsConfigDict(env_file=".env")
    PORT: int = 8000


settings = Settings()
