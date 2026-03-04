from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    name: str
    echo_sql: bool = False
    model_config = SettingsConfigDict(
        env_prefix="PG__", extra="ignore", env_file=".env"
    )

    def get_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.name}"
        )

class TgBotConfig(BaseSettings):
    token: str

    model_config = SettingsConfigDict(
        env_prefix="TG_BOT_", extra="ignore", env_file=".env"
    )

class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()  # type: ignore
    tg_bot: TgBotConfig = TgBotConfig() # type: ignore

    debug: bool = False
    app_name: str = "mood_diary"


    def get_db_config(self) -> DatabaseConfig:
        return self.db

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings() # type: ignore
