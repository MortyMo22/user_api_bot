# log.py
import os
from datetime import datetime

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

def log_message(user_id, username, user_text, bot_response):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = os.path.join(LOG_DIR, f"{user_id}.log")

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {username} ({user_id})\n")
        f.write(f"USER: {user_text}\n")
        f.write(f"BOT: {bot_response}\n")
        f.write("-" * 50 + "\n")
