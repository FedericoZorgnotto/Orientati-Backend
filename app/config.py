from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    app_name: str = "Vallauri orientamento"
    DATABASE_URL: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30
    VERSION: str
    SECRET_KEY: str
    SENTRY_DSN: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
