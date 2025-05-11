#!/bin/bash

case "$1" in
  worker)
    exec rq worker --with-scheduler --url redis://$REDIS_HOST:$REDIS_PORT default
    ;;
  scheduler)
    exec rqscheduler --host $REDIS_HOST --port $REDIS_PORT --db 0
    ;;
  schedule_jobs)
    exec python -m data_processing_framework
    ;;
  *)
    echo "Unknown command: $1"
    exit 1
    ;;
esac
