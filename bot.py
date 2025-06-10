import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from pymongo import MongoClient
import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB setup
mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client[Config.DB_NAME]
files_collection = db["files"]
channels_collection = db["channels"]


app = Client(
    "file_index_bot",
    api_id=25492855,          # Optional
    api_hash=61876db014de51a4ace6b169608be4f1,      # Optional
    bot_token=Config.BOT_TOKEN,
    workers=100
)


@app.on_message(filters.command("index") & filters.channel)
async def index_files(client: Client, message: Message):
    """Index all files in the channel where /index is sent"""
    if message.from_user and message.from_user.id not in Config.ADMIN_IDS:
        return
    
    channel_id = message.chat.id
    channel_title = message.chat.title
    
    # Check if channel is already indexed
    channel_data = channels_collection.find_one({"channel_id": channel_id})
    if not channel_data:
        channels_collection.insert_one({
            "channel_id": channel_id,
            "channel_title": channel_title,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now()
        })
    else:
        channels_collection.update_one(
            {"channel_id": channel_id},
            {"$set": {"updated_at": datetime.datetime.now()}}
        )
    
    await message.reply_text(f"🚀 Starting to index files in {channel_title}...")
    
    total_files = 0
    async for msg in client.iter_history(channel_id):
        if msg.document or msg.video or msg.audio:
            file_id = msg.document.file_id if msg.document else msg.video.file_id if msg.video else msg.audio.file_id
            file_name = msg.document.file_name if msg.document else msg.video.file_name if msg.video else msg.audio.file_name
            
            # Check if file already exists
            existing_file = files_collection.find_one({
                "channel_id": channel_id,
                "file_id": file_id
            })
            
            if not existing_file:
                files_collection.insert_one({
                    "channel_id": channel_id,
                    "channel_title": channel_title,
                    "file_id": file_id,
                    "file_name": file_name,
                    "file_type": msg.document.mime_type if msg.document else msg.video.mime_type if msg.video else msg.audio.mime_type,
                    "file_size": msg.document.file_size if msg.document else msg.video.file_size if msg.video else msg.audio.file_size,
                    "caption": msg.caption if msg.caption else file_name,
                    "message_id": msg.message_id,
                    "thumbnail": msg.video.thumbs[0].file_id if msg.video and msg.video.thumbs else None,
                    "date": msg.date,
                    "indexed_at": datetime.datetime.now()
                })
                total_files += 1
    
    await message.reply_text(f"✅ Indexing complete! Added {total_files} new files from {channel_title}.")

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = """
📚 **File Index Bot Help**

/addchannel - Add a channel to index
/index - Index all files in the current channel
/listchannels - List all indexed channels
/help - Show this help message

🔗 Web Interface: {Config.BASE_URL}
"""
    await message.reply_text(help_text)

if __name__ == "__main__":
    logger.info("Starting File Index Bot...")
    app.run()
