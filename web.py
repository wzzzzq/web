import os
import re
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, template_folder="templates")
CORS(app)

LOG_FILE = "server.log"  # 你可以改成 Gunicorn 日志路径，比如 `/var/log/gunicorn.log`

# ✅ 读取日志文件中的所有消息
def get_messages_from_logs():
    if not os.path.exists(LOG_FILE):
        return []

    messages = []
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            match = re.search(r"Received message: (.+)", line)  # 提取消息
            if match:
                time_match = re.search(r"\[(\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2})", line)  # 提取时间
                log_time = time_match.group(1) if time_match else "Unknown Time"
                messages.append({"time": log_time, "text": match.group(1)})

    return messages[::-1]  # 让最新的消息显示在最上面

# ✅ 记录消息到日志文件
def log_message(text):
    timestamp = datetime.now().strftime("[%d/%b/%Y:%H:%M:%S]")  # 生成时间格式
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{timestamp} Received message: {text}\n")

@app.route('/')
def index():
    return render_template('index.html', messages=get_messages_from_logs())

@app.route('/send-message', methods=['POST'])
def handle_message():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    log_message(user_message)  # 把消息写入日志

    return jsonify({"response": "Message received", "messages": get_messages_from_logs()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
