from flask_login import UserMixin
import json
import os
from config import Config

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 共通のデータ操作関数
def load_shopping_list():
    with open(Config.SHOPPING_LIST_FILE, "r") as f:
        return json.load(f)

def save_shopping_list(data):
    with open(Config.SHOPPING_LIST_FILE, "w") as f:
        json.dump(data, f)

def load_recipes():
    with open(Config.RECIPE_FILE, "r") as f:
        return json.load(f)

def save_recipes(data):
    with open(Config.RECIPE_FILE, "w") as f:
        json.dump(data, f)

def load_menu():
    with open(Config.MENU_FILE, "r") as f:
        return json.load(f)

def save_menu(data):
    with open(Config.MENU_FILE, "w") as f:
        json.dump(data, f)
