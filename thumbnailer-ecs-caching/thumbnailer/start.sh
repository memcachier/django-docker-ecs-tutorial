#!/bin/bash

EC2_REGION=$(curl -s http://169.254.170.2/v2/metadata | grep TaskARN | cut -d: -f5)

function get_param() {
    aws ssm get-parameters --names $1 --with-decryption --region $EC2_REGION | \
        grep Value | cut -d: -f2- | tr -d '" ,'
}

export MEMCACHIER_SERVER=$(get_param thumbnailer.memcachier-server)
export MEMCACHIER_USERNAME=$(get_param thumbnailer.memcachier-username)
export MEMCACHIER_PASSWORD=$(get_param thumbnailer.memcachier-password)

echo Starting Gunicorn...
gunicorn --bind=0.0.0.0:8000 \
         --workers=3 --worker-class=gevent \
         --access-logfile '-' --error-logfile '-' --capture-output \
         thumbnailer.wsgi
