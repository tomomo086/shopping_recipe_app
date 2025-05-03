#!/bin/bash
sleep 15  # アプリが起動するのを待つ
cd "$(dirname "$0")"  # スクリプトのディレクトリに移動

while true; do
    # ngrokを起動（既存の設定を使用）
    ngrok start shopping_list --log=ngrok.log &
    NGROK_PID=$!
    
    # 2時間実行したら再起動
    sleep 7200
    kill $NGROK_PID
    sleep 30
done
