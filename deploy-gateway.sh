#!/bin/bash

# check for env variables
# exit 1 if any missing
# $GATEWAY_HOST $GATEWAY_USER $GATEWAY_HOST_KEY $GATEWAY_FQDN

if [[ -z $GATEWAY_HOST || -z $GATEWAY_USER || -z $GATEWAY_FQDN || -z $GATEWAY_HOST_KEY ]]; then
    echo "-- ERROR: missing one or more required environment variables --"
    exit 1
fi

echo $GATEWAY_HOST_KEY > /root/.ssh/gw-key && chmod 400 /root/.ssh/gw-key

ansible-playbook ansible/configure-nginx.yml -i "$GATEWAY_HOST," -u $GATEWAY_USER --private-key /root/.ssh/gw-key
