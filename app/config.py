from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # URI Templates (Runtime Derivation)
    # These can be overridden in your .env file without code changes
    gemini_uri_template: str = "https://generativelanguage.googleapis.com/v1beta/models/${model_id}:generateContent?key=${api_key}"
    openai_uri_template: str = "https://api.openai.com/v1/chat/completions"
    claude_uri_template: str = "https://api.anthropic.com/v1/messages"
    
    # API Keys (Required)
    google_api_key: str
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Financial Governance
    default_max_output_tokens: int = 512

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
