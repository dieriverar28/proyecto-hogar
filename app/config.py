from pydantic_settings import BaseSettings, SettingsConfigDict
#BaseSettings de Pydantic lee automáticamente las variables desde un archivo 
# .env o desde variables de entorno del sistema

class Settings(BaseSettings):
    # Base de datos
    database_url: str

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()