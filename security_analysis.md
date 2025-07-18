# セキュリティ分析レポート：機密情報の調査結果

## 🔍 調査概要
このアプリケーションにおいて、公開してはいけない機密情報を調査した結果をまとめます。

## ⚠️ 発見された機密情報

### 1. ハードコードされたパスワード・認証情報

#### 📍 config.py (25行目、29-30行目)
```python
SECRET_KEY = os.environ.get('SECRET_KEY', '019d9cecc66e13a00f1b47b298995dbd')

USERS = {
    os.environ.get('APP_USERNAME', 'kaimono'): {
        'password': os.environ.get('APP_PASSWORD', 'kuutaro5412')
    }
}
```

**問題点:**
- Flask SECRET_KEYのデフォルト値がハードコード
- アプリケーションのデフォルトユーザー名 `kaimono` がハードコード
- デフォルトパスワード `kuutaro5412` がハードコード

### 2. Ngrokトークン関連情報

#### 📍 README.md (107行目、227行目、233行目)
```yaml
authtoken: "あなたのngrokトークン"
```
```bash
./ngrok authtoken あなたのトークン
```

**問題点:**
- ngrokの認証トークンがプレースホルダーとして記載されているが、実際の環境では実際のトークンが設定される可能性

### 3. 実際のngrok URL（公開URL）

#### 📍 current_url.txt
```
url=https://e75b-126-100-67-1.ngrok-free.app
```

#### 📍 nohup.out
```
最新URL: url=https://b4a9-126-100-67-1.ngrok-free.app
```

**問題点:**
- アプリケーションの実際の公開URLが平文で保存されている
- 外部からアクセス可能なエンドポイントが露出している

### 4. メール設定（環境変数依存だが設定箇所は特定）

#### 📍 config.py (40-42行目)
```python
GMAIL_ADDRESS = os.environ.get('GMAIL_ADDRESS', '')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD', '')
TO_ADDRESSES = os.environ.get('TO_ADDRESSES', '').split(',') if os.environ.get('TO_ADDRESSES') else []
```

#### 📍 send_email.py (66行目)
```python
server.login(Config.GMAIL_ADDRESS, Config.GMAIL_PASSWORD)
```

**問題点:**
- Gmailのアドレスとアプリパスワードが環境変数として設定される
- 送信先メールアドレスのリストが環境変数として設定される

### 5. ホスト設定

#### 📍 config.py (35行目)
```python
HOST = os.environ.get('HOST', "0.0.0.0")
```

**問題点:**
- デフォルトで全インターフェースでリッスン（0.0.0.0）

## 🚨 リスク評価

### 高リスク
1. **ハードコードされたパスワード** (`kuutaro5412`) - すぐに変更が必要
2. **ハードコードされたSECRET_KEY** - すぐに変更が必要
3. **実際のngrok URL** - 公開されているアクセスポイント

### 中リスク
1. **デフォルトユーザー名** (`kaimono`) - 推測しやすい
2. **メール設定の環境変数** - 適切に管理されていれば問題ないが注意が必要

### 低リスク
1. **ホスト設定** - 意図的な設定と思われるが確認が必要

## 📝 推奨対策

### 即座に対応すべき項目
1. **config.py** のハードコードされたデフォルト値をすべて削除
2. **current_url.txt** と **nohup.out** をGitignoreに追加
3. 強力なパスワードとSECRET_KEYの生成・設定

### 長期的な改善項目
1. 環境変数の適切な管理体制の確立
2. 認証システムの強化検討
3. ログファイルの適切な管理

## 📂 関連ファイル一覧
- `config.py` - メイン設定ファイル（要修正）
- `send_email.py` - メール送信機能
- `current_url.txt` - ngrok URL保存ファイル（要Gitignore追加）
- `nohup.out` - 実行ログファイル（要Gitignore追加）
- `README.md` - ドキュメント（ngrokトークンの記述あり）
- `shopping_list_routes.py` - ログイン処理実装
- `templates/shopping/login.html` - ログインフォーム

---
*調査日時: 2024年12月*
*調査対象: ショッピング・レシピアプリケーション*