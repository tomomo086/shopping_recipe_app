import smtplib
import time
import os
from email.mime.text import MIMEText
from config import Config

def get_ngrok_url():
    try:
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ngrok.log")
        
        if not os.path.exists(log_file):
            print(f"ngrokログファイルが見つかりません: {log_file}")
            return None
        
        with open(log_file, "r") as f:
            lines = f.readlines()
        
        for line in reversed(lines):
            if "started tunnel" in line and "url=" in line:
                url = line.split("url=")[-1].strip()
                return url
        
        print("ngrokログファイルからURLが見つかりませんでした")
        return None
    
    except Exception as e:
        print(f"ngrok URLの取得中にエラーが発生しました: {e}")
        return None

def save_current_url(url):
    try:
        if not url:
            print("URLが空のため保存しません")
            return False
        
        current_url_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "current_url.txt")
        
        with open(current_url_file, "w") as f:
            f.write(f"url={url}")
        
        print(f"最新URLを保存しました: {url}")
        return True
    
    except Exception as e:
        print(f"URLの保存中にエラーが発生しました: {e}")
        return False

def send_email(url):
    if not Config.GMAIL_ADDRESS or not Config.GMAIL_PASSWORD or not Config.TO_ADDRESSES:
        print("メール設定が不完全です。環境変数を確認してください。")
        return False
    
    if not url:
        print("URLが空のためメールを送信しません")
        return False
    
    msg = MIMEText(f"新しい買い物＆レシピアプリのアドレス: {url}")
    msg["Subject"] = "新しい買い物＆レシピアプリのアドレス"
    msg["From"] = Config.GMAIL_ADDRESS
    msg["To"] = ", ".join(Config.TO_ADDRESSES)
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
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
    
    # 前回のURLを読み込む
    try:
        current_url_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "current_url.txt")
        
        if os.path.exists(current_url_file):
            with open(current_url_file, "r") as f:
                last_url = f.read().strip().replace("url=", "")
                print(f"前回のURL: {last_url}")
    except Exception as e:
        print(f"前回のURLの読み込み中にエラーが発生しました: {e}")
    
    try:
        while True:
            url = get_ngrok_url()
            
            if url and url != last_url:
                if send_email(url):
                    save_current_url(url)
                    last_url = url
            
            time.sleep(60)  # 1分ごとにチェック
    except KeyboardInterrupt:
        print("プログラムを終了します")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
