from flask_login import UserMixin
import json
import os
import shutil
from config import Config

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 共通のデータ操作関数
def load_shopping_list():
    try:
        with open(Config.SHOPPING_LIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"買い物リストファイルが見つかりません: {Config.SHOPPING_LIST_FILE}")
        return {"食品": [], "日用品": []}
    except json.JSONDecodeError:
        print(f"買い物リストファイルの形式が不正です: {Config.SHOPPING_LIST_FILE}")
        # バックアップを確認
        backup_file = f"{Config.SHOPPING_LIST_FILE}.bak"
        if os.path.exists(backup_file):
            try:
                with open(backup_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"食品": [], "日用品": []}
    except Exception as e:
        print(f"買い物リストファイルの読み込み中にエラーが発生しました: {e}")
        return {"食品": [], "日用品": []}

def save_shopping_list(data):
    try:
        # バックアップを作成
        if os.path.exists(Config.SHOPPING_LIST_FILE):
            backup_file = f"{Config.SHOPPING_LIST_FILE}.bak"
            try:
                shutil.copy2(Config.SHOPPING_LIST_FILE, backup_file)
            except Exception as e:
                print(f"バックアップの作成に失敗しました: {e}")
                
        with open(Config.SHOPPING_LIST_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"買い物リストファイルの保存中にエラーが発生しました: {e}")
        return False

def load_recipes():
    try:
        with open(Config.RECIPE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"レシピファイルが見つかりません: {Config.RECIPE_FILE}")
        return {"recipes": []}
    except json.JSONDecodeError:
        print(f"レシピファイルの形式が不正です: {Config.RECIPE_FILE}")
        # バックアップを確認
        backup_file = f"{Config.RECIPE_FILE}.bak"
        if os.path.exists(backup_file):
            try:
                with open(backup_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"recipes": []}
    except Exception as e:
        print(f"レシピファイルの読み込み中にエラーが発生しました: {e}")
        return {"recipes": []}

def save_recipes(data):
    try:
        # バックアップを作成
        if os.path.exists(Config.RECIPE_FILE):
            backup_file = f"{Config.RECIPE_FILE}.bak"
            try:
                shutil.copy2(Config.RECIPE_FILE, backup_file)
            except Exception as e:
                print(f"バックアップの作成に失敗しました: {e}")
                
        with open(Config.RECIPE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"レシピファイルの保存中にエラーが発生しました: {e}")
        return False

def load_menu():
    try:
        with open(Config.MENU_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"メニューファイルが見つかりません: {Config.MENU_FILE}")
        return {"weeks": []}
    except json.JSONDecodeError:
        print(f"メニューファイルの形式が不正です: {Config.MENU_FILE}")
        # バックアップを確認
        backup_file = f"{Config.MENU_FILE}.bak"
        if os.path.exists(backup_file):
            try:
                with open(backup_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"weeks": []}
    except Exception as e:
        print(f"メニューファイルの読み込み中にエラーが発生しました: {e}")
        return {"weeks": []}

def save_menu(data):
    try:
        # バックアップを作成
        if os.path.exists(Config.MENU_FILE):
            backup_file = f"{Config.MENU_FILE}.bak"
            try:
                shutil.copy2(Config.MENU_FILE, backup_file)
            except Exception as e:
                print(f"バックアップの作成に失敗しました: {e}")
                
        with open(Config.MENU_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"メニューファイルの保存中にエラーが発生しました: {e}")
        return False
