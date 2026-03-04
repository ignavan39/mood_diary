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


class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig() # type: ignore
    debug: bool = False

    def get_db_config(self) -> DatabaseConfig:
        return self.db

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
