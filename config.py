from pydantic_settings import BaseSettings, SettingsConfigDict
import dotenv

class Settings(BaseSettings):
    host: str
    port: int

    redis_host: str
    redis_port: int

    postgresql_host: str
    postgresql_port: int
    postgresql_database_name: str
    postgresql_password: str
    postgresql_user: str


    model_config = SettingsConfigDict(env_file=dotenv.find_dotenv(), extra = "allow")


settings = Settings()

