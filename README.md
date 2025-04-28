# 買い物リストアプリケーション - GitHub README

以下が、GitHubリポジトリ用のREADME.mdの内容です。初心者にも分かりやすく、詳細な説明を含めました：

```markdown
# 買い物リストアプリケーション

## 概要
このアプリケーションは、食品と日用品の買い物リストをカテゴリ別に管理できるウェブアプリです。Raspberry Piで動作し、USBドライブにデータを保存します。ngrokを使用して外部からアクセス可能です。

## 特徴
- ユーザー認証システム（ログイン/ログアウト機能）
- 食品・日用品の2カテゴリでの管理
- アイテムの追加・削除・全削除機能
- レスポンシブデザイン（PCとモバイル両対応）
- USBドライブへのデータ保存
- 定期的なバックアップ機能
- ngrokによる外部アクセス
- URL変更時の自動メール通知

## 技術スタック
- **バックエンド**: Python 3, Flask, Flask-Login
- **フロントエンド**: HTML, CSS, JavaScript, Font Awesome
- **データ保存**: JSON
- **デプロイ環境**: Raspberry Pi
- **外部公開**: ngrok

## インストール方法

### 前提条件
- Raspberry Pi (Raspberry Pi OS)
- Python 3.6以上
- pip
- ngrok アカウントとセットアップ
- USBドライブ

### セットアップ手順

1. リポジトリをクローン
```bash
git clone https://github.com/[ユーザー名]/shopping_list.git
cd shopping_list
```

2. 仮想環境を作成してアクティベート
```bash
python -m venv venv
source venv/bin/activate  # Linuxの場合
```

3. 必要なパッケージをインストール
```bash
pip install flask flask-login
```

4. USBドライブをマウント
   - Raspberry PiにUSBドライブを接続
   - マウントポイントを確認し、必要に応じて`app.py`のDATA_FILE変数を修正

5. アプリケーションを起動
```bash
python app.py
```

## 使用方法

1. ブラウザで `http://[RaspberryPiのIPアドレス]:5000` にアクセス
2. ユーザー名 `kaimono` とパスワード `kuutaro5412` でログイン
3. アイテム追加フォームからカテゴリを選択してアイテムを追加
4. 必要に応じてアイテムを削除または全削除

## 外部アクセスの設定

### ngrokの設定
1. ngrokをインストール
2. 以下のコマンドを実行して、ポート5000のトンネルを設定
```bash
ngrok http --subdomain=shopping_list 5000
```

### 自動起動の設定
1. `crontab -e` を実行
2. 以下の行を追加（アプリケーションとngrokの自動起動）
```
@reboot cd /home/tomo/shopping_list && python app.py
@reboot cd /home/tomo/shopping_list && ./start_ngrok.sh
@reboot cd /home/tomo/shopping_list && python send_email.py
```

## バックアップの設定
1. `backup.sh` に実行権限を付与
```bash
chmod +x backup.sh
```

2. cronに定期バックアップを設定（毎日午前2時に実行する例）
```
0 2 * * * /home/tomo/shopping_list/backup.sh
```

## 開発環境のセットアップ
1. リポジトリをクローン
2. 仮想環境を作成してアクティベート
3. 必要なパッケージをインストール
4. USBドライブのマウントパスを調整（開発マシンに合わせて）
5. `app.py` の以下の行を編集して開発モードで実行
```python
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
```

## プロジェクト構造
- `app.py`: メインアプリケーションコード
- `templates/`: HTMLテンプレートファイル
- `static/`: CSS、JavaScript、画像ファイル
- `backup.sh`: バックアップスクリプト
- `start_ngrok.sh`: ngrok起動スクリプト
- `send_email.py`: URL変更通知スクリプト

## セキュリティに関する注意
- 本番環境では、ハードコードされたパスワードを環境変数や設定ファイルに移動してください
- ngrok URLは定期的に変更されるため、`send_email.py` で通知されます
- 重要なデータは定期的にバックアップしてください

## 今後の改善点
- パスワードのハッシュ化
- 複数ユーザー対応
- カテゴリの追加・編集機能
- アイテムの優先度や数量の管理
- データベースへの移行（SQLiteなど）
```

このREADMEはあなたのプロジェクトの概要、特徴、インストール・使用方法などを詳細に説明しており、初心者の方でも理解しやすい形で情報を提供しています。実際のGitHubリポジトリに追加することで、プロジェクトの理解や共有が容易になります。

セキュリティ上の理由から、実際の公開リポジトリでは、パスワードや個人的なメールアドレスは削除または環境変数に移行することをお勧めします。
