from flask import Blueprint, render_template, request, redirect, url_for
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in Config.USERS and Config.USERS[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('shopping.index'))
        else:
            return render_template('login.html', error='ユーザー名またはパスワードが間違っています')
    return render_template('login.html')

# ログアウト
@shopping_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('shopping.login'))

# 買い物リストページ
@shopping_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    items = load_shopping_list()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            item = request.form.get("item")
            category = request.form.get("category")
            if item and category in ["食品", "日用品"]:
                items[category].append(item)
                save_shopping_list(items)
        elif action == "delete":
            category = request.form.get("category")
            index = int(request.form.get("index"))
            if category in items and 0 <= index < len(items[category]):
                items[category].pop(index)
                save_shopping_list(items)
        elif action == "clear":
            category = request.form.get("category")
            if category in items:
                items[category] = []
                save_shopping_list(items)
        return redirect(url_for("shopping.index"))
    return render_template('index.html', items=items)
