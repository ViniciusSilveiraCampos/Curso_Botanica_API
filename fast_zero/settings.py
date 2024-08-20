from pydantic_settings import BaseSettings, SettingsConfigDict


# Configuração do banco de dados
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra="ignore"
    )

    DATABASE_URL: str
    SECRET_KEY: str
    algorithm: str
    ACESS_TOKEN_EXPIRE_MINUTES: int
