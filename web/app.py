from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from config import Config
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# MongoDB setup
mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client[Config.DB_NAME]
files_collection = db["files"]
channels_collection = db["channels"]

@app.route("/")
def index():
    channels = list(channels_collection.find().sort("channel_title", 1))
    selected_channel = request.args.get("channel")
    
    files = []
    channel_title = "All Files"
    
    if selected_channel:
        files = list(files_collection.find({"channel_id": int(selected_channel)}).sort("date", -1))
        channel_data = channels_collection.find_one({"channel_id": int(selected_channel)})
        if channel_data:
            channel_title = channel_data["channel_title"]
    else:
        files = list(files_collection.find().sort("date", -1).limit(100))
    
    return render_template(
        "index.html",
        channels=channels,
        files=files,
        channel_title=channel_title,
        selected_channel=selected_channel,
        base_url="https://involved-valenka-dhndhajsjs-39484c8d.koyeb.app", 
        config=Config
    )

if __name__ == "__main__":
    app.run(host=Config.WEB_HOST, port=Config.WEB_PORT, debug=True)
