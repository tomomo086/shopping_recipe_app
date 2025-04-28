import smtplib
import time
from email.mime.text import MIMEText
import os

GMAIL_ADDRESS = "tomo.nfm08@gmail.com"
GMAIL_PASSWORD = "dtan yqgv vgkv nvwp"
TO_ADDRESSES = ["tomo.nfm08@gmail.com", "y.yes.nyo.n@gmail.com"]

def get_ngrok_url():
    log_file = "/home/tomo/shopping_list/ngrok.log"
    if not os.path.exists(log_file):
        return None
    with open(log_file, "r") as f:
        lines = f.readlines()
    for line in reversed(lines):
        if "started tunnel" in line:
            url = line.split("url=")[-1].strip()
            return url
    return None

def send_email(url):
    msg = MIMEText(f"新しいngrok URL: {url}")
    msg["Subject"] = "新しい買い物リストのアドレス"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = ", ".join(TO_ADDRESSES)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    time.sleep(30)  # ネットワークが安定するまで待機
    last_url = ""
    while True:
        url = get_ngrok_url()
        if url and url != last_url:
            send_email(url)
            last_url = url
        time.sleep(60)  # 1分ごとにチェック
