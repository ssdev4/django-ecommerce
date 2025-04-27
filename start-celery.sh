#!/bin/bash

# start-celery.sh
# Run Celery worker + Flower together with clean shutdown on Ctrl+C

# Exit immediately if any command fails
set -e

# Function to cleanly stop both Celery worker and Flower
cleanup() {
    echo ""
    echo "🛑 Stopping Celery worker and Flower..."
    kill $worker_pid
    kill $flower_pid
    exit 0
}

# Trap Ctrl+C (SIGINT) to call cleanup()
trap cleanup SIGINT

echo "🚀 Starting Celery worker..."
celery -A ecommerce_project worker --loglevel=info &
worker_pid=$!

# Optional small wait to ensure worker is ready
sleep 3

echo "🌸 Starting Flower dashboard..."
celery -A ecommerce_project flower --port=5555 &
flower_pid=$!

echo ""
echo "✅ Celery worker PID: $worker_pid"
echo "✅ Flower PID: $flower_pid"
echo "🌍 Flower UI: http://localhost:5555"
echo ""
echo "Press Ctrl+C to stop everything."

# Wait forever (until trap catches Ctrl+C)
wait
