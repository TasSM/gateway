#!/bin/bash

cd /

INVENTORY_FILE=/gateway/ansible/inventory.ini
KEY_FILE=/root/.ssh/gw-key
TIMEOUT=300

if [[ -z $GATEWAY_HOST || -z $GATEWAY_USER || -z $GATEWAY_FQDN || -z $GATEWAY_HOST_KEY || -z $CERTBOT_EMAIL ]]; then
    echo "-- ERROR: missing one or more required environment variables --"
    exit 1
fi

# Create necessary files
mkdir -p /root/.ssh && echo $GATEWAY_HOST_KEY > $KEY_FILE && chmod 400 $KEY_FILE
echo "[webservers]" > $INVENTORY_FILE && echo $GATEWAY_HOST >> $INVENTORY_FILE

if [[ ! -z $HOSTED_ZONE_ID ]]; then

    if [[ -z $AWS_ACCESS_KEY_ID || -z $AWS_SECRET_ACCESS_KEY ]]; then
        echo "-- ERROR: missing one or more required variables for Route53 deployment --"
        exit 1
    fi

    echo "-- Creating DNS record in Route53 --"
    /usr/bin/python3 /gateway/scripts/main.py
    if [[ $? != 0 ]]; then
        echo "-- ERROR: Route53 Operation Failed --"
        exit 1
    fi

    # Await DNS resolution of new record
    echo "-- Attempting DNS resolution of newly created record --"
    while true; do
        let TIMEOUT-=30
        sleep 30
        if [[ ! -z $( nslookup $GATEWAY_FQDN | grep $GATEWAY_HOST ) ]]; then \
            echo "-- Resolved new DNS record $GATEWAY_FQDN for $GATEWAY_HOST --" \ 
            break
        fi
        if [[ $TIMEOUT -le 0 ]]; then
            echo "ERROR: Timeout reached - could not resolve after 300 seconds"
            exit 1
        fi
        echo "-- Awaiting resolution: Timeout in $TIMEOUT --"
    done

fi

ansible-playbook /gateway/ansible/configure-nginx.yml -i $INVENTORY_FILE  -u $GATEWAY_USER --private-key $KEY_FILE
