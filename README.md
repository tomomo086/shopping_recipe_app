# 🛒 買い物リスト＆レシピ管理アプリ

![Platform: Raspberry Pi | Web](https://img.shields.io/badge/Platform-Raspberry%20Pi%20%7C%20Web-green.svg)
![Language: Python | HTML/CSS/JS](https://img.shields.io/badge/Language-Python%20%7C%20HTML%2FCSS%2FJS-orange.svg)
![AI: Grok3 | Claude4 | Cursor](https://img.shields.io/badge/AI-Grok3%20%7C%20Claude4%20%7C%20Cursor-blue.svg)
![Method: VibCoding](https://img.shields.io/badge/Method-VibCoding-red.svg)
![Status: Portfolio](https://img.shields.io/badge/Status-Portfolio-purple.svg)

## 📸 デモ・スクリーンショット

### 🖼️ アプリケーション画面
<!-- ここに実際のアプリ画面のスクリーンショットを2枚追加してください -->
<!-- 例: ![買い物リスト画面](images/shopping_list_screenshot.png) -->
<!-- 例: ![レシピ管理画面](images/recipe_management_screenshot.png) -->

### 🎥 動作デモ動画
<!-- ここにXの動画リンクを追加してください -->
<!-- 例: [📱 アプリ動作デモ動画](https://x.com/mirai_sousiyo39/status/...) -->

## 📋 プロジェクト概要

**AI駆動開発による最新技術を活用した、共働き世帯向けの買い物・献立管理システム**

本プロジェクトは、AIによるバイブコーディング（AI駆動による最新の開発手法）を活用し、Raspberry Pi 3B+上で動作する家庭向けWebアプリケーションです。共働き世帯の情報共有効率化と献立の悩みを解決することを目的として設計されています。

> ⚠️ **注意**: これはポートフォリオ・学習目的の作品です。配布や商用利用は想定しておりません。

### 🎯 解決する課題
- **情報共有の非効率性**: 夫婦間での買い物リストや献立の情報共有が困難
- **献立の悩み**: 毎日の献立決めに時間を取られる
- **買い物の重複**: 同じ食材を重複して購入してしまう
- **レシピ管理の分散**: インスタグラム等のSNSで見つけたレシピの一元管理ができない

### 💡 設計思想
- **AI駆動開発**: Grok3、Claude4、ClaudeCode、Cursorを活用した効率的な開発
- **家庭サーバー**: Raspberry Pi 3B+による自宅でのWebサーバー運用
- **共働き配慮**: 夫婦間の情報共有を最優先としたUI/UX設計
- **外部連携**: SNSで見つけたレシピの一元管理機能

## 🚀 主要機能

### 📝 買い物リスト管理
- 食品・日用品のカテゴリ別管理
- レシピからの材料一括追加
- 週間メニューからの買い物リスト自動生成
- リアルタイム同期（夫婦間での共有）

### 👨‍🍳 レシピ管理
- レシピの検索・分類・保存
- 材料・調味料・手順の詳細管理
- タグ機能による分類
- インスタグラム等のSNSレシピの一元管理

### 📅 週間メニュープランナー
- 一週間分の朝食・昼食・夕食の計画
- 過去のメニュー履歴の閲覧
- メニューから買い物リストへの一括変換
- 栄養バランスの考慮

### 🌐 外部アクセス機能
- ngrokによる外部からのアクセス提供
- URL変更時の自動メール通知
- スマートフォンからの外出先アクセス対応

### 🔄 自動化機能
- 定期バックアップ（USBメモリ対応）
- 自動起動・停止（crontab管理）
- ngrokの自動再起動による安定性確保

## 🛠️ 技術スタック

### 開発手法
- **AI駆動開発**: Grok3 → Claude4 → ClaudeCode → Cursor の進化
- **バイブコーディング**: AIとの対話による効率的な開発
- **継続的改善**: AIフィードバックによる機能拡張

### バックエンド
- **Python 3.6+**: メイン開発言語
- **Flask**: Webフレームワーク
- **Flask-Login**: 認証システム
- **python-dotenv**: 環境変数管理

### フロントエンド
- **HTML5/CSS3**: レスポンシブデザイン
- **JavaScript**: 動的UI機能
- **Font Awesome**: アイコンライブラリ

### インフラ・運用
- **Raspberry Pi 3B+**: ホームサーバー
- **ngrok**: 外部アクセス提供
- **crontab**: 自動化スケジューリング
- **USBメモリ**: ハードが劣化してもSDカードより交換が容易

### データ管理
- **JSON**: 軽量データストレージ
- **環境変数**: セキュリティ設定
- **Git**: バージョン管理

## 🏗️ アーキテクチャ

### ファイル構造
```
shopping_recipe_app/
├── app.py                    # メインアプリケーション
├── config.py                 # 設定管理（環境変数対応）
├── models.py                 # データモデル
├── recipe_routes.py          # レシピ機能
├── shopping_list_routes.py   # 買い物リスト機能
├── send_email.py             # メール通知機能
├── backup.sh                 # バックアップスクリプト
├── start_ngrok.sh            # ngrok起動スクリプト
├── static/                   # 静的ファイル
│   ├── css/style.css         # レスポンシブスタイル
│   └── js/script.js          # 動的UI機能
└── templates/                # テンプレート
    ├── layout.html           # 共通レイアウト
    ├── recipe/               # レシピ関連ページ
    └── shopping/             # 買い物リスト関連ページ
```

### データフロー
1. **ユーザー認証** → Flask-Loginによるセッション管理
2. **データ操作** → JSONファイルによる永続化
3. **外部アクセス** → ngrokによるトンネリング
4. **自動化** → crontabによるスケジューリング

## 📱 ユーザー体験設計

### 共働き世帯向けの配慮
- **シンプルなUI**: 忙しい夫婦でも直感的に操作可能
- **リアルタイム同期**: 夫婦間での情報共有を即座に反映
- **外出先アクセス**: スマートフォンからの外出先での買い物リスト確認
- **SNS連携**: インスタグラム等で見つけたレシピの簡単保存

### レスポンシブデザイン
- **デスクトップ**: 詳細な情報表示と効率的な操作
- **タブレット**: キッチンでのレシピ表示に最適化
- **スマートフォン**: 外出先での買い物リスト確認に最適化

## 🚀 デプロイメント

### Raspberry Pi 3B+での運用
```bash
# 必要なライブラリをインストール
sudo apt-get update
sudo apt-get install -y python3-pip git

# Flaskと必要なライブラリをインストール
pip3 install flask flask-login python-dotenv

# プロジェクトをクローン
git clone https://github.com/[ユーザー名]/shopping_recipe_app.git
cd shopping_recipe_app

# 環境変数設定
cp .env.example .env
nano .env  # 必要に応じて編集

# データディレクトリを作成
mkdir -p data

# アプリ実行
python3 app.py
```

### 自動化設定（crontab）
```bash
# 7:00にアプリ、ngrok、メール送信を起動
0 7 * * * /usr/bin/python3 /home/tomo/shopping_recipe_app/app.py >> /home/tomo/shopping_recipe_app/app.log 2>&1 &
1 7 * * * /bin/bash /home/tomo/shopping_recipe_app/start_ngrok.sh >> /home/tomo/shopping_recipe_app/ngrok.log 2>&1 &
2 7 * * * /usr/bin/python3 /home/tomo/shopping_recipe_app/send_email.py >> /home/tomo/shopping_recipe_app/email.log 2>&1 &

# 0:00にアプリ、ngrokを停止
0 0 * * * /usr/bin/pkill -9 python3
0 0 * * * /usr/bin/pkill -9 ngrok

# 毎朝3:00にバックアップを実行
0 3 * * * /bin/bash /home/tomo/shopping_recipe_app/backup.sh
```

## 📊 開発プロセス

### AI駆動開発の流れ
1. **要件定義**: 共働き世帯の課題分析
2. **AI設計**: Grok3による初期アーキテクチャ設計
3. **実装**: Claude4によるコア機能実装
4. **最適化**: ClaudeCodeによるコード品質向上
5. **継続改善**: Cursorによる機能拡張とバグ修正

### 開発の特徴
- **迅速なプロトタイピング**: AIによる効率的なコード生成
- **品質保証**: AIによるコードレビューと改善提案
- **継続的学習**: 新しいAI技術の積極的活用

## 📈 成果・効果

### 技術的成果
- **AI駆動開発の実践**: 最新のAI技術を活用した効率的な開発
- **家庭サーバーの構築**: Raspberry Piによる実用的なWebサービス運用
- **セキュリティ対策**: 本番環境での安全な運用

### 実用的効果
- **情報共有の効率化**: 夫婦間での買い物・献立情報の一元管理
- **時間の節約**: 献立決めと買い物の効率化
- **重複購入の防止**: 買い物リストによる計画的な購入

## 📄 ライセンス

MIT License

---

## 👨‍💻 開発者情報

**開発者**: tomomo086(@mirai_sousiyo39)  
**技術**: Grok3 → Claude4 → ClaudeCode → Cursor  
**ハードウェア**: Raspberry Pi 3B+  
**目的**: 共働き世帯の生活効率化

### 🔗 関連リンク

- [tomomo086: Github](https://github.com/tomomo086)
- [@mirai_sousiyo39: X](https://x.com/mirai_sousiyo39)

---

*このプロジェクトは、AI駆動開発による最新技術を活用したポートフォリオ作品です。*
