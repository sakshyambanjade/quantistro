from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Placeholder for future API keys or DB URLs
    yahoo_finance_api_key: str = ""
    alpha_vantage_api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
