from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User, load_shopping_list, save_shopping_list
from config import Config

# Blueprintの作成
shopping_bp = Blueprint('shopping', __name__, template_folder='templates/shopping')

# テンプレートでenumerate関数を使えるようにする
@shopping_bp.app_template_global()
def enumerate(iterable, start=0):
    return [(i, item) for i, item in __builtins__.enumerate(iterable, start)]

# ログインページ
@shopping_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    try:
        if request.method == 'POST':
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            if username in Config.USERS and Config.USERS[username]['password'] == password:
                user = User(username)
                login_user(user)
                return redirect(url_for('shopping.index'))
            else:
                error = 'ユーザー名またはパスワードが間違っています'
    except Exception as e:
        print(f"ログイン処理中にエラーが発生しました: {e}")
        error = '予期しないエラーが発生しました。管理者に連絡してください。'
    
    return render_template('login.html', error=error)

# ログアウト
@shopping_bp.route('/logout')
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        print(f"ログアウト処理中にエラーが発生しました: {e}")
    
    return redirect(url_for('shopping.login'))

# 買い物リストページ
@shopping_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    error = None
    items = load_shopping_list()
    
    if request.method == "POST":
        try:
            action = request.form.get("action", "")
            
            if action == "add":
                item = request.form.get("item", "").strip()
                category = request.form.get("category", "")
                
                if item and category in ["食品", "日用品"]:
                    items[category].append(item)
                    if save_shopping_list(items):
                        print(f"アイテムを追加しました: {category} - {item}")
                    else:
                        error = "買い物リストの保存に失敗しました"
                else:
                    error = "アイテム名とカテゴリを正しく入力してください"
            
            elif action == "delete":
                category = request.form.get("category", "")
                index = request.form.get("index", "")
                
                if category in items and index.isdigit():
                    index = int(index)
                    if 0 <= index < len(items[category]):
                        removed_item = items[category].pop(index)
                        if save_shopping_list(items):
                            print(f"アイテムを削除しました: {category} - {removed_item}")
                        else:
                            error = "買い物リストの保存に失敗しました"
                    else:
                        error = "無効なインデックスです"
                else:
                    error = "無効なカテゴリまたはインデックスです"
            
            elif action == "clear":
                category = request.form.get("category", "")
                
                if category in items:
                    items[category] = []
                    if save_shopping_list(items):
                        print(f"カテゴリをクリアしました: {category}")
                    else:
                        error = "買い物リストの保存に失敗しました"
                else:
                    error = "無効なカテゴリです"
        
        except Exception as e:
            print(f"買い物リスト処理中にエラーが発生しました: {e}")
            error = "予期しないエラーが発生しました"
        
        return redirect(url_for("shopping.index"))
    
    return render_template('index.html', items=items, error=error)
