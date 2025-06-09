import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Telegram API ID and Hash (Optional for bot-only use)
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = "FileIndexBot"
    
    # Web Server Configuration
    WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
    WEB_PORT = int(os.getenv("WEB_PORT", 5000))
    
    # Base URL for web interface
    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
    
    # Admin user IDs (comma separated)
    ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
