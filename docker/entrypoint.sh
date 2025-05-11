#!/bin/bash

case "$1" in
  worker)
    exec rq worker --with-scheduler --url redis://$REDIS_HOST:$REDIS_PORT default
    ;;
  scheduler)
    exec python -m data_processing_framework
    ;;
  dashboard)
    exec rq-dashboard --redis-url redis://$REDIS_HOST:$REDIS_PORT
    ;;
  *)
    echo "Unknown command: $1"
    exit 1
    ;;
esac