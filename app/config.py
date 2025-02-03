from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    app_name: str = "Vallauri orientamento"
    DATABASE_URL: str = "sqlite:///./database.db"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 600
    refresh_token_expire_days: int = 30
    VERSION: str = "0.1.0"
    SECRET_KEY: str = "secret"
    SENTRY_DSN: str = ""
    MONGODB_CONNECTION_STRING: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "orientati"
    MONGODB_STATS_COLLECTION: str = "stats"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
