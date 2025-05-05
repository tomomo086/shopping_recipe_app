from flask import Flask, redirect, url_for, flash
from flask_login import LoginManager
import os
import time
import json
import sys
import logging
from logging.handlers import RotatingFileHandler
from config import Config
from models import User

app = Flask(__name__)
app.config.from_object(Config)

# ロギングの設定
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'), 
        maxBytes=1024 * 1024 * 5,  # 5MB
        backupCount=3
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    # Werkzeugのロガー設定
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(file_handler)

setup_logging()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "shopping.login"

@login_manager.user_loader
def load_user(user_id):
    if user_id in app.config['USERS']:
        return User(user_id)
    return None

# USB mount waiting (for Raspberry Pi)
def wait_for_usb():
    # 開発環境では自動的にデータディレクトリを作成
    if not os.path.exists(app.config['USB_PATH']):
        try:
            os.makedirs(app.config['USB_PATH'], exist_ok=True)
            app.logger.info(f"データディレクトリを作成しました: {app.config['USB_PATH']}")
            return True
        except Exception as e:
            app.logger.error(f"データディレクトリの作成に失敗しました: {e}")
            return False
    return True

# JSONファイルの初期化
def init_json_files():
    try:
        # 買い物リストファイルの初期化
        if not os.path.exists(app.config['SHOPPING_LIST_FILE']):
            with open(app.config['SHOPPING_LIST_FILE'], "w", encoding="utf-8") as f:
                json.dump({"食品": [], "日用品": []}, f, ensure_ascii=False, indent=2)
            app.logger.info(f"買い物リストファイルを作成しました: {app.config['SHOPPING_LIST_FILE']}")
        
        # レシピファイルの初期化
        if not os.path.exists(app.config['RECIPE_FILE']):
            with open(app.config['RECIPE_FILE'], "w", encoding="utf-8") as f:
                json.dump({"recipes": []}, f, ensure_ascii=False, indent=2)
            app.logger.info(f"レシピファイルを作成しました: {app.config['RECIPE_FILE']}")
        
        # 週間メニューファイルの初期化
        if not os.path.exists(app.config['MENU_FILE']):
            with open(app.config['MENU_FILE'], "w", encoding="utf-8") as f:
                json.dump({"weeks": []}, f, ensure_ascii=False, indent=2)
            app.logger.info(f"週間メニューファイルを作成しました: {app.config['MENU_FILE']}")
        
        return True
    except Exception as e:
        app.logger.error(f"JSONファイルの初期化中にエラーが発生しました: {e}")
        return False

# 各Blueprintをここでインポート（循環インポートを避けるため）
from shopping_list_routes import shopping_bp
from recipe_routes import recipe_bp

# 各機能をBlueprintとして登録
app.register_blueprint(shopping_bp, url_prefix='/shopping')
app.register_blueprint(recipe_bp, url_prefix='/recipe')

# ルートURLへのリダイレクト
@app.route('/')
def index():
    return redirect(url_for('shopping.index'))

if __name__ == "__main__":
    try:
        app.logger.info("アプリケーションを起動しています...")
        if not wait_for_usb():
            app.logger.error("USBドライブまたはデータディレクトリが利用できません。アプリケーションを終了します。")
            sys.exit(1)
            
        if not init_json_files():
            app.logger.error("JSONファイルの初期化に失敗しました。アプリケーションを終了します。")
            sys.exit(1)
            
        app.logger.info(f"アプリケーションを起動しています: http://{app.config['HOST']}:{app.config['PORT']}")
        app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
    except Exception as e:
        app.logger.error(f"エラーが発生しました: {e}")
        sys.exit(1)
