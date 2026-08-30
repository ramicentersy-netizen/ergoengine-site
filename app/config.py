import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ErgoEngine - AI Affiliate Authority Hub"
    BASE_URL: str = "http://localhost:8000"
    DATABASE_URL: str = "sqlite:///./data/engine.db"
    
    # Affiliate Settings
    AMAZON_TRACKING_TAG: str = "ergoengine-20"
    AFFILIATE_DISCLOSURE_TEXT: str = (
        "ErgoEngine is reader-supported. When you buy through links on our site, "
        "we may earn an affiliate commission at no extra cost to you."
    )
    
    # AI Generation Settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # Telegram Notifications Settings
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    
    # Quality & Compliance Guardrails
    MIN_WORD_COUNT: int = 600
    FORBID_FIRST_PERSON_EXPERIENCE: bool = True
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
