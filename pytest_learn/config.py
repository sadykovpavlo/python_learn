from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    base_url: str
    database_url: str
    model_config = SettingsConfigDict(extra='ignore')
