from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    newsbot_mode: str = "demo"
    tavily_api_key: str | None = None
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    max_retries: int = 2
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

settings = Settings()
