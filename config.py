import os

class Config:
    # パス設定
    # 開発環境用（GitHub上での開発時）
    USB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    
    # 本番環境用（Raspberry Pi - USBドライブ使用時）
    # USB_PATH = "/media/tomo/piusb"
    
    SHOPPING_LIST_FILE = os.path.join(USB_PATH, "shopping_list.json")
    RECIPE_FILE = os.path.join(USB_PATH, "recipes.json")
    MENU_FILE = os.path.join(USB_PATH, "weekly_menu.json")
    
    # Flask設定
    SECRET_KEY = '019d9cecc66e13a00f1b47b298995dbd'  # 本番環境では変更してください
    
    # ユーザー設定
    USERS = {'kaimono': {'password': 'kuutaro5412'}}
    
    # アプリケーション設定
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True  # 開発中はTrue、本番環境ではFalseに変更
    
    # メール通知設定
    GMAIL_ADDRESS = "tomo.nfm08@gmail.com"  # 実際に使用するGmailアドレスに変更
    GMAIL_PASSWORD = "dtan yqgv vgkv nvwp"  # Gmailアプリパスワード（セキュリティのため実際の環境では変更）
    TO_ADDRESSES = ["tomo.nfm08@gmail.com", "y.yes.nyo.n@gmail.com"]  # 通知先メールアドレス
