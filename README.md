# 買い物リスト＆レシピアプリ

## 概要
このアプリケーションは、買い物リスト管理とレシピ検索・管理を統合したWebアプリです。Raspberry Piで動作し、ngrokを使用して外部からアクセスできます。

## 特徴
- 買い物リスト管理（食品・日用品）
- レシピの追加・検索・管理
- レシピから買い物リストへのアイテム追加
- 週間メニュープランナー
- ngrokによる外部アクセス
- URL変更時の自動メール通知
- 定期バックアップ機能

## 技術スタック
- バックエンド: Python, Flask, Flask-Login
- フロントエンド: HTML, CSS, JavaScript, Font Awesome
- データ保存: JSON
- デプロイ環境: Raspberry Pi
- 外部公開: ngrok

## インストール方法

### 前提条件
- Raspberry Pi (Raspberry Pi OS)
- Python 3.6以上
- pip
- ngrok アカウントとセットアップ
- USBドライブ（オプション）

### セットアップ手順

1. リポジトリをクローン
```bash
git clone https://github.com/[ユーザー名]/shopping-recipe-app.git
cd shopping-recipe-app
