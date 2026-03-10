from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisCacheConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="REDIS__",
        env_file=".env",
        case_sensitive=False,
    )

    host: str
    port: int = 6379
    password: str
    db: int = 0


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

    @property
    def url(self) -> str:
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
    tg_bot: TgBotConfig = TgBotConfig()  # type: ignore
    redis_cache: RedisCacheConfig = RedisCacheConfig()  # type: ignore

    debug: bool = False
    log_level: str = "INFO"
    app_name: str = "mood_diary"

    def get_db_config(self) -> DatabaseConfig:
        return self.db

    def get_redis_cache_config(self) -> RedisCacheConfig:
        return self.redis_cache

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()  # type: ignore
