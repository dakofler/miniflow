#!/bin/bash

case "$1" in
  worker)
    exec rq worker --with-scheduler --url redis://$REDIS_HOST:$REDIS_PORT default
    ;;
  dashboard)
    exec rq-dashboard --redis-url redis://$REDIS_HOST:$REDIS_PORT
    ;;
  scheduler)
    exec python -m miniflow
    ;;
  *)
    echo "Unknown command: $1"
    exit 1
    ;;
esac