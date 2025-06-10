import re, time, os
from os import environ



class Config(object):
    API_ID = os.environ.get("API_ID", "25492855")
    API_HASH = os.environ.get("API_HASH", "61876db014de51a4ace6b169608be4f1")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7421749280:AAE4DWOVNP7VTck6ZZyFNmyrH_6fOssmg1s")

    # MongoDB Configuration
    MONGO_URI = os.environ.get("MONGO_URI","mongodb+srv://Yash_607:Yash_607@cluster0.r3s9sbo.mongodb.net/?retryWrites=true&w=majority")
    DB_NAME = os.environ.get("DB_NAME", "FileIndexBot") 
    
    # Web Server Configuration
    WEB_HOST = os.environ.get("WEB_HOST", "0.0.0.0")
    WEB_PORT = int(os.environ.get("WEB_PORT", 8080))
    
    # Base URL for web interface
    BASE_URL = os.environ.get("BASE_URL", "")
    
    # Admin user IDs (comma separated)
    ADMIN_IDS = [int(id) for id in os.environ.get("ADMIN_IDS", "6359874284").split(",") if id]
