#!/bin/bash

case "$1" in
  worker)
    exec rq worker --with-scheduler --url redis://redis:6379 high default low
    ;;
  dashboard)
    exec rq-dashboard --redis-url redis://redis:6379
    ;;
  *)
    echo "Unknown command: $1"
    exit 1
    ;;
esac