from flask import Flask, redirect, url_for
from flask_login import LoginManager
import os
import time
import json
import sys
from config import Config
from models import User

app = Flask(__name__)
app.config.from_object(Config)

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
            print(f"データディレクトリを作成しました: {app.config['USB_PATH']}")
            return True
        except Exception as e:
            print(f"データディレクトリの作成に失敗しました: {e}")
            return False
    return True

# JSONファイルの初期化
def init_json_files():
    try:
        # 買い物リストファイルの初期化
        if not os.path.exists(app.config['SHOPPING_LIST_FILE']):
            with open(app.config['SHOPPING_LIST_FILE'], "w") as f:
                json.dump({"食品": [], "日用品": []}, f)
            print(f"買い物リストファイルを作成しました: {app.config['SHOPPING_LIST_FILE']}")
        
        # レシピファイルの初期化
        if not os.path.exists(app.config['RECIPE_FILE']):
            with open(app.config['RECIPE_FILE'], "w") as f:
                json.dump({"recipes": []}, f)
            print(f"レシピファイルを作成しました: {app.config['RECIPE_FILE']}")
        
        # 週間メニューファイルの初期化
        if not os.path.exists(app.config['MENU_FILE']):
            with open(app.config['MENU_FILE'], "w") as f:
                json.dump({"weeks": []}, f)
            print(f"週間メニューファイルを作成しました: {app.config['MENU_FILE']}")
        
        return True
    except Exception as e:
        print(f"JSONファイルの初期化中にエラーが発生しました: {e}")
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
        if not wait_for_usb():
            print("USBドライブまたはデータディレクトリが利用できません。アプリケーションを終了します。")
            sys.exit(1)
            
        if not init_json_files():
            print("JSONファイルの初期化に失敗しました。アプリケーションを終了します。")
            sys.exit(1)
            
        print(f"アプリケーションを起動しています: http://{app.config['HOST']}:{app.config['PORT']}")
        app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)
