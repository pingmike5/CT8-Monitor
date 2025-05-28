import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import re
import logging
import threading
from flask import Flask, jsonify

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
URL = "https://www.ct8.pl/"
LAST_COUNT = None

@app.route("/")
def index():
    return "Hallo,world."

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

def get_current_time():
    utc_now = datetime.now(pytz.utc)
    tz = pytz.timezone('Asia/Shanghai')
    local_time = utc_now.astimezone(tz)
    return local_time.strftime("%Y-%m-%d %H:%M:%S (UTC+8)")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {str(e)}")

def fetch_account_count():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.select("span.button.is-large.is-flexible")
        for el in elements:
            text = el.get_text(strip=True)
            match = re.search(r'(\d+)\s*/\s*(\d+)', text)
            if match:
                return f"{match.group(1)} / {match.group(2)}"
        return None
    except Exception as e:
        logger.error(f"Error fetching count: {str(e)}")
        return None

def monitor_loop():
    global LAST_COUNT
    logger.info("Monitoring loop started")
    while True:
        try:
            current = fetch_account_count()
            if current:
                if current != LAST_COUNT:
                    logger.info(f"Detected change: {current}")
                    current_time = get_current_time()
                    send_telegram_message(f"🎉 CT8账户变化: {current} 🎉\n{current_time}")
                    LAST_COUNT = current
                else:
                    logger.debug(f"No change: {current}")
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            logger.error(f"Error in monitoring loop: {str(e)}")
            time.sleep(60)  # 出错后等待1分钟再重试

if __name__ == "__main__":
    from waitress import serve
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    logger.info("Starting web server...")
    serve(app, host="0.0.0.0", port=7860)
