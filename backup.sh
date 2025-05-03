#!/bin/bash
# バックアップ先ディレクトリ
BACKUP_DIR="/home/tomo/backup"
# 現在の日時を取得（例: 20250422_1200）
TIMESTAMP=$(date +"%Y%m%d_%H%M")
# ソースディレクトリ
SOURCE_DIR="/home/tomo/shopping-recipe-app"
# 一時ディレクトリ（crontab用）
TEMP_DIR="/tmp/backup_temp"

# 一時ディレクトリを作成
mkdir -p "$TEMP_DIR"

# crontabの内容をファイルに保存
crontab -l > "$TEMP_DIR/crontab_backup_$TIMESTAMP.txt" 2>/dev/null
# エラーが出る場合（crontabが未設定の場合）は空ファイルを作成
if [ $? -ne 0 ]; then
    touch "$TEMP_DIR/crontab_backup_$TIMESTAMP.txt"
fi

# バックアップディレクトリが存在しない場合は作成
mkdir -p "$BACKUP_DIR"

# shopping-recipe-appディレクトリの全ファイルとcrontabをバックアップ
tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" -C "$SOURCE_DIR" . -C "$TEMP_DIR" "crontab_backup_$TIMESTAMP.txt"

# 一時ファイルを削除
rm -rf "$TEMP_DIR"

# 30日以上前のバックアップファイルを削除
find "$BACKUP_DIR" -type f -mtime +30 -exec rm {} \;

echo "バックアップが完了しました: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
