#!/bin/bash
sleep 15  # アプリが起動するのを待つ
while true; do
    ngrok start shopping_list --log=/home/tomo/shopping_list/ngrok.log &
    NGROK_PID=$!
    sleep 7200
    kill $NGROK_PID
    sleep 30
done
