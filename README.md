# 買い物リスト＆レシピアプリ レジュメ

## 1. プロジェクト概要

本プロジェクトは、家庭での買い物計画とレシピ管理を一元化するWebアプリケーションです。Raspberry Pi上で動作し、以下の主要機能を提供します：

- 食品・日用品の買い物リスト管理
- レシピの追加・検索・閲覧機能
- レシピから買い物リストへの材料追加機能
- 週間メニュープランナー
- ngrokを使用した外部アクセス機能
- URL変更時の自動メール通知
- 定期バックアップ機能

## 2. 技術スタック

- **バックエンド**：Python 3.6+, Flask, Flask-Login
- **フロントエンド**：HTML, CSS, JavaScript, Font Awesome
- **データ保存**：JSON形式
- **デプロイ環境**：Raspberry Pi
- **外部公開**：ngrok
- **追加ライブラリ**：python-dotenv

## 3. ファイル構造

```
shopping-recipe-app/
├── .gitignore                    # Git無視ファイル設定
├── README.md                     # プロジェクト説明ファイル
├── app.py                        # メインアプリケーション
├── backup.sh                     # バックアップスクリプト
├── config.py                     # 設定ファイル
├── current_url.txt               # 現在のngrok URL保存ファイル
├── models.py                     # データモデル
├── ngrok.log                     # ngrokログファイル
├── nohup.out                     # バックグラウンド実行ログ
├── recipe_routes.py              # レシピ機能のルート定義
├── send_email.py                 # メール通知機能
├── shopping_list_routes.py       # 買い物リスト機能のルート定義
├── start_ngrok.sh                # ngrok起動スクリプト
├── static/                       # 静的ファイル格納ディレクトリ
│   ├── css/
│   │   └── style.css             # スタイルシート
│   └── js/
│       └── script.js             # JavaScript
└── templates/                    # テンプレートディレクトリ
    ├── layout.html               # 共通レイアウト
    ├── recipe/                   # レシピ関連テンプレート
    │   ├── add.html              # レシピ追加ページ
    │   ├── detail.html           # レシピ詳細ページ
    │   ├── index.html            # レシピ一覧ページ
    │   └── menu_planner.html     # 週間メニューページ
    └── shopping/                 # 買い物リスト関連テンプレート
        ├── index.html            # 買い物リストページ
        └── login.html            # ログインページ
```

実行時には自動的に以下のディレクトリとファイルが作成されます：

```
shopping-recipe-app/
└── data/                         # データ保存ディレクトリ（開発環境用）
    ├── shopping_list.json        # 買い物リストデータ
    ├── recipes.json              # レシピデータ
    └── weekly_menu.json          # 週間メニューデータ
```

本番環境（Raspberry Pi）では、USBメモリがマウントされている場合、`data/`ディレクトリの代わりにUSBメモリ上にこれらのJSONファイルが保存されます。

また、ngrok設定ファイルは以下の場所に存在します（システムの隠しディレクトリ）：
```
/home/tomo/.ngrok2/ngrok.yml
```

## 4. 主要コンポーネントの説明

### 4.1 Python コア機能

#### app.py
アプリケーションのエントリーポイント。Flaskアプリケーションの初期化、ルートの登録、USBマウント待機、JSONファイル初期化などを行います。

#### config.py
環境設定を管理。デフォルト設定と環境変数からの上書き機能を提供。開発環境と本番環境（Raspberry Pi）の切り替えにも対応。

#### models.py
データモデルと共通データ操作関数を提供。ユーザー認証モデルと、買い物リスト・レシピ・週間メニューの読み書き機能を実装。

#### shopping_list_routes.py
買い物リスト機能のルート定義。ログイン/ログアウト処理と買い物リスト管理（追加・削除・全削除）を実装。

#### recipe_routes.py
レシピ機能のルート定義。レシピの検索・詳細表示・追加・削除、買い物リストへの材料追加、週間メニュープランナー機能を実装。

### 4.2 スクリプト機能

#### backup.sh
バックアップスクリプト。アプリケーションフォルダとcrontab設定を定期的にバックアップし、古いバックアップを自動削除。

#### send_email.py
ngrokのURL変更を監視し、変更があった場合にメール通知を送信。定期的にngrokログをチェックして最新URLを取得。

#### start_ngrok.sh
ngrokを起動・管理するスクリプト。`/home/tomo/.ngrok2/ngrok.yml`の既存設定を使用して「shopping_list」という名前のトンネルを開始します。アプリケーションディレクトリ内の`ngrok.log`にログを出力し、2時間（7200秒）ごとに再起動して安定性を確保します。

ngrok設定ファイル（`/home/tomo/.ngrok2/ngrok.yml`）の内容：
```yaml
version: "2"
authtoken: "あなたのngrokトークン"
tunnels:
  shopping_list:
    addr: 5000
    proto: http
```

### 4.3 フロントエンド

#### static/css/style.css
アプリ全体のスタイルを定義。レスポンシブデザインに対応し、スマートフォンでも使いやすいUIを提供。

#### static/js/script.js
クライアントサイドの動的機能を実装。特にレシピ追加画面での材料・手順の動的追加/削除機能を提供。

#### templates/layout.html
全ページ共通のレイアウトテンプレート。ナビゲーションバーとコンテナを定義。

## 5. 主要機能の詳細

### 5.1 認証システム
- Flask-Loginを使用したシンプルな認証システム
- config.py内でユーザー名とパスワードを設定（環境変数対応）
- セッション管理と保護されたルートへのアクセス制御

### 5.2 買い物リスト管理
- 食品と日用品の2カテゴリで管理
- アイテムの追加・削除・カテゴリごとの全削除機能
- JSONファイルによるデータ永続化
- シンプルで使いやすいUI

### 5.3 レシピ管理
- レシピの検索（タイトル・材料・タグで検索可能）
- 詳細な情報（材料・調味料・手順・メモ）の管理
- レシピの追加・削除機能
- タグによる分類

### 5.4 材料連携機能
- レシピ詳細画面から買い物リストへの材料追加機能
- 調味料は任意で追加可能（チェックボックスで選択）
- 週間メニューからまとめて買い物リスト生成機能

### 5.5 週間メニュープランナー
- 一週間分の朝食・昼食・夕食メニューを計画
- 各食事にレシピを割り当て
- 過去のメニュー計画の閲覧
- メニューから買い物リスト一括生成機能

### 5.6 外部アクセス機能
- ngrokを使用した外部からのアクセス提供
- URL変更時の自動メール通知機能
- 定期的なngrok再起動による安定性確保

### 5.7 バックアップ機能
- 定期的なアプリケーションデータのバックアップ
- crontab設定の保存
- 30日以上経過したバックアップの自動削除

## 6. スケジュール設定（crontab）

以下のcrontab設定で、アプリの自動起動・停止とバックアップを管理します：

```bash
# 電源オン時に残プロセスをクリア
@reboot /usr/bin/pkill -9 python3
@reboot /usr/bin/pkill -9 ngrok

# 7:00にアプリ、ngrok、メール送信を起動
0 7 * * * /usr/bin/python3 /home/tomo/shopping-recipe-app/app.py >> /home/tomo/shopping-recipe-app/app.log 2>&1 &
1 7 * * * /bin/bash /home/tomo/shopping-recipe-app/start_ngrok.sh >> /home/tomo/shopping-recipe-app/ngrok.log 2>&1 &
2 7 * * * /usr/bin/python3 /home/tomo/shopping-recipe-app/send_email.py >> /home/tomo/shopping-recipe-app/email.log 2>&1 &

# 0:00にアプリ、ngrokを停止
0 0 * * * /usr/bin/pkill -9 python3
0 0 * * * /usr/bin/pkill -9 ngrok

# 毎朝3:00にバックアップを実行
0 3 * * * /bin/bash /home/tomo/shopping-recipe-app/backup.sh
```

## 7. インストール・セットアップ手順

### 7.1 前提条件
- Raspberry Pi (Raspberry Pi OS)
- Python 3.6以上
- pip
- ngrokアカウントとセットアップ
- USBドライブ（オプション）

### 7.2 基本セットアップ
```bash
# 必要なライブラリをインストール
sudo apt-get update
sudo apt-get install -y python3-pip git

# Flaskと必要なライブラリをインストール
pip3 install flask flask-login python-dotenv

# プロジェクトをクローン
git clone https://github.com/[ユーザー名]/shopping-recipe-app.git
cd shopping-recipe-app

# 環境変数設定（オプション）
cp .env.example .env
nano .env  # 必要に応じて編集

# データディレクトリを作成
mkdir -p data

# アプリ実行
python3 app.py
```

### 7.3 ngrokセットアップ
```bash
# ngrokをダウンロード（ARM版）
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.tgz
tar xvzf ngrok-v3-stable-linux-arm.tgz

# ngrokを認証（要アカウント）
./ngrok authtoken あなたのトークン

# ngrok設定ファイルを作成
mkdir -p ~/.ngrok2
cat > ~/.ngrok2/ngrok.yml << EOF
version: "2"
authtoken: "あなたのngrokトークン"
tunnels:
  shopping_list:
    addr: 5000
    proto: http
EOF

# 設定ファイルの確認
cat ~/.ngrok2/ngrok.yml

# 起動テスト
./ngrok start shopping_list
```

### 7.4 自動起動設定
```bash
# 実行権限付与
chmod +x app.py backup.sh start_ngrok.sh send_email.py

# crontabに追加
crontab -e

# 上記のcrontab設定を追加
```

## 8. トラブルシューティング

- **USBマウントエラー**: config.pyでローカルディレクトリを使用するよう設定を変更
- **ngrok接続問題**: 
  - start_ngrok.shの再起動間隔を調整
  - ~/.ngrok2/ngrok.ymlの設定を確認
  - ngrokのトークン認証が正しく行われているか確認
- **メール送信エラー**: Gmailの設定でアプリパスワードを確認
- **バックアップ失敗**: バックアップディレクトリの権限を確認
- **JSONファイルエラー**: data/ディレクトリの権限とファイル形式を確認

## 9. 今後の拡張可能性

- データベース導入（SQLite/MySQL）
- ユーザー管理機能の拡充（複数ユーザー対応）
- レシピ画像のアップロード機能
- 食品の賞味期限管理機能
- モバイルアプリ連携（APIの実装）
- 栄養情報の追加と栄養バランス計算機能
- 外部レシピAPIとの連携

---

このレジュメは買い物リスト＆レシピアプリの全体像を把握するための文書です。実際の実装では、セキュリティ強化や機能拡張などのさらなる改善が可能です。
