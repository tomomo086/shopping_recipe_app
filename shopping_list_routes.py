from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from models import User, load_shopping_list, save_shopping_list
from config import Config
import logging

# Blueprintの作成
shopping_bp = Blueprint('shopping', __name__, template_folder='templates/shopping')
logger = logging.getLogger(__name__)

# テンプレートでenumerate関数を使えるようにする
@shopping_bp.app_template_global()
def enumerate(iterable, start=0):
    # シンプルな実装に修正
    return enumerate(iterable, start)

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
                logger.info(f"ユーザーがログインしました: {username}")
                return redirect(url_for('shopping.index'))
            else:
                error = 'ユーザー名またはパスワードが間違っています'
                logger.warning(f"ログイン失敗: {username}")
    except Exception as e:
        logger.error(f"ログイン処理中にエラーが発生しました: {e}")
        error = '予期しないエラーが発生しました。管理者に連絡してください。'
    
    return render_template('login.html', error=error)

# ログアウト
@shopping_bp.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        logger.info(f"ユーザーがログアウトしました")
    except Exception as e:
        logger.error(f"ログアウト処理中にエラーが発生しました: {e}")
    
    return redirect(url_for('shopping.login'))

# 買い物リストページ
@shopping_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    try:
        # データ読み込み
        items = load_shopping_list()
        error = None
        
        if request.method == "POST":
            try:
                action = request.form.get("action", "")
                
                if action == "add":
                    item = request.form.get("item", "").strip()
                    category = request.form.get("category", "")
                    
                    if item and category in ["食品", "日用品"]:
                        items[category].append(item)
                        if save_shopping_list(items):
                            logger.info(f"アイテムを追加しました: {category} - {item}")
                            flash(f"{category}に「{item}」を追加しました", "success")
                        else:
                            error = "買い物リストの保存に失敗しました"
                            flash(error, "error")
                    else:
                        error = "アイテム名とカテゴリを正しく入力してください"
                        flash(error, "error")
                
                elif action == "delete":
                    category = request.form.get("category", "")
                    index = request.form.get("index", "")
                    
                    if category in items and index.isdigit():
                        index = int(index)
                        if 0 <= index < len(items[category]):
                            removed_item = items[category].pop(index)
                            if save_shopping_list(items):
                                logger.info(f"アイテムを削除しました: {category} - {removed_item}")
                                flash(f"{category}から「{removed_item}」を削除しました", "success")
                            else:
                                error = "買い物リストの保存に失敗しました"
                                flash(error, "error")
                        else:
                            error = "無効なインデックスです"
                            flash(error, "error")
                    else:
                        error = "無効なカテゴリまたはインデックスです"
                        flash(error, "error")
                
                elif action == "clear":
                    category = request.form.get("category", "")
                    
                    if category in items:
                        items[category] = []
                        if save_shopping_list(items):
                            logger.info(f"カテゴリをクリアしました: {category}")
                            flash(f"{category}をクリアしました", "success")
                        else:
                            error = "買い物リストの保存に失敗しました"
                            flash(error, "error")
                    else:
                        error = "無効なカテゴリです"
                        flash(error, "error")
            
            except Exception as e:
                logger.error(f"買い物リスト処理中にエラーが発生しました: {e}")
                error = "予期しないエラーが発生しました"
                flash(error, "error")
            
            return redirect(url_for("shopping.index"))
        
        # 買い物リストとエラー情報（あれば）をテンプレートに渡す
        # データ構造を確認
        if not isinstance(items, dict):
            logger.error(f"買い物リストの形式が不正です: {type(items)}")
            items = {"食品": [], "日用品": []}
        
        # 必要なカテゴリが存在することを確認
        for category in ["食品", "日用品"]:
            if category not in items:
                items[category] = []
        
        return render_template('index.html', items=items, error=error)
    
    except Exception as e:
        # 重大なエラーが発生した場合は、ログに記録してシンプルなエラーページを表示
        logger.error(f"買い物リスト表示中に致命的なエラーが発生しました: {e}")
        current_app.logger.error(f"買い物リスト表示中に致命的なエラーが発生しました: {e}")
        return render_template('error.html', error=f"エラーが発生しました: {str(e)}")
