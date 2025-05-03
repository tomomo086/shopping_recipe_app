import smtplib
import time
import os
from email.mime.text import MIMEText
from config import Config

def get_ngrok_url():
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ngrok.log")
    if not os.path.exists(log_file):
        return None
    
    with open(log_file, "r") as f:
        lines = f.readlines()
    
    for line in reversed(lines):
        if "started tunnel" in line and "url=" in line:
            url = line.split("url=")[-1].strip()
            return url
    return None

def save_current_url(url):
    current_url_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "current_url.txt")
    with open(current_url_file, "w") as f:
        f.write(f"url={url}")
    print(f"最新URL: url={url}")

def send_email(url):
    msg = MIMEText(f"新しい買い物＆レシピアプリのアドレス: {url}")
    msg["Subject"] = "新しい買い物＆レシピアプリのアドレス"
    msg["From"] = Config.GMAIL_ADDRESS
    msg["To"] = ", ".join(Config.TO_ADDRESSES)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(Config.GMAIL_ADDRESS, Config.GMAIL_PASSWORD)
            server.send_message(msg)
            print(f"通知メール送信成功: {url}")
            return True
    except Exception as e:
        print(f"メール送信エラー: {e}")
        return False

if __name__ == "__main__":
    time.sleep(30)  # ネットワークが安定するまで待機
    last_url = ""
    
    current_url_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "current_url.txt")
    if os.path.exists(current_url_file):
        with open(current_url_file, "r") as f:
            last_url = f.read().strip().replace("url=", "")
    
    while True:
        url = get_ngrok_url()
        if url and url != last_url:
            send_email(url)
            save_current_url(url)
            last_url = url
        time.sleep(60)  # 1分ごとにチェック
