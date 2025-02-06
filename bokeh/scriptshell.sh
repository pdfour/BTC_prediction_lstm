#!/bin/bash


cd "/var/services/homes/user" 

URL="https://contract.mexc.com/api/v1/contract/kline/BTC_USDT"


while true; do
    date_now=$(date +"%Y-%m-%d %H:%M:%S.%6N")
    echo "$date_now,$(curl -s "$URL" | jq -r '" \(.data.date[-1]), \(.data.open[-1]), \(.data.high[-1]), \(.data.low[-1]), \(.data.vol[-1])"')" >> "btc.csv"
done
