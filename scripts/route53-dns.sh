#!/bin/bash

echo "-- Creating DNS record in Route53 --"
/usr/bin/python3 ./main.py

# Await DNS to resolve
ECHO "-- Attempting DNS resolution of newly created record --"
TIMEOUT=300
while true; do
    TIMEOUT-=5
    sleep 5
    if [[ ! -z $(nslookup $RECORD_NAME | grep $DNS_TARGET)]]; then
        echo "-- Resolved new DNS record $RECORD_NAME for $DNS_TARGET --"
        exit 0
    fi
    if [[ $TIMEOUT -le 0 ]]; then
        echo "ERROR: Timeout reached - could not resolve after 300 seconds"
        exit 1
    fi
done