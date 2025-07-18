import os

# python-dotenvをオプション扱いに
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("環境変数を.envファイルから読み込みました")
except ImportError:
    print("python-dotenvがインストールされていないため、.envファイルからの環境変数読み込みをスキップします")

class Config:
    # パス設定
    # 開発環境用（GitHub上での開発時）
    USB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    
    # 本番環境用（Raspberry Pi - USBドライブ使用時）
    # 環境変数でUSB_PATHを上書き可能
    if os.environ.get('USB_PATH'):
        USB_PATH = os.environ.get('USB_PATH')
    
    SHOPPING_LIST_FILE = os.path.join(USB_PATH, "shopping_list.json")
    RECIPE_FILE = os.path.join(USB_PATH, "recipes.json")
    MENU_FILE = os.path.join(USB_PATH, "weekly_menu.json")
    
    # Flask設定
    # 重要: 本番環境では必ず環境変数 SECRET_KEY を設定してください
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    
    # ユーザー設定 - 環境変数またはデフォルト値を使用
    # 重要: 本番環境では必ず環境変数 APP_USERNAME と APP_PASSWORD を設定してください
    USERS = {
        os.environ.get('APP_USERNAME', 'demo_user'): {
            'password': os.environ.get('APP_PASSWORD', 'change_me_password')
        }
    }
    
    # アプリケーション設定
    HOST = os.environ.get('HOST', "0.0.0.0")
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # メール通知設定
    GMAIL_ADDRESS = os.environ.get('GMAIL_ADDRESS', '')
    GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD', '')
    TO_ADDRESSES = os.environ.get('TO_ADDRESSES', '').split(',') if os.environ.get('TO_ADDRESSES') else []
