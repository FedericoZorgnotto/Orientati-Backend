from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    app_name: str = "Vallauri orientamento"
    database_url: str
    secret_key: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
