from flask import Flask, request, render_template, redirect, url_for
import os
import time
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = '019d9cecc66e13a00f1b47b298995dbd'
DATA_FILE = "/media/tomo/piusb/shopping_list.json"

# テンプレートでenumerate関数を使えるようにする（修正版）
@app.template_global()
def enumerate(iterable, start=0):
    return [(i, item) for i, item in __builtins__.enumerate(iterable, start)]

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'kaimono': {'password': 'kuutaro5412'}}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# USB mount waiting (for Raspberry Pi)
timeout = 30
start_time = time.time()
while not os.path.exists("/media/tomo/piusb"):
    if time.time() - start_time > timeout:
        raise FileNotFoundError(f"USB not found after {timeout} seconds")
    time.sleep(5)

# JSON file initialization
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"食品": [], "日用品": []}, f)

# JSON file read/write functions
def load_items():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_items(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='ユーザー名またはパスワードが間違っています')
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Main shopping list page
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    items = load_items()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            item = request.form.get("item")
            category = request.form.get("category")
            if item and category in ["食品", "日用品"]:
                items[category].append(item)
                save_items(items)
        elif action == "delete":
            category = request.form.get("category")
            index = int(request.form.get("index"))
            if category in items and 0 <= index < len(items[category]):
                items[category].pop(index)
                save_items(items)
        elif action == "clear":
            category = request.form.get("category")
            if category in items:
                items[category] = []
                save_items(items)
        return redirect(url_for("index"))
    return render_template('index.html', items=items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
