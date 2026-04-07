#!/bin/bash

# PaperLens Backend Startup Script

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Install dependencies if needed
# pip install -r requirements.txt

# Start the FastAPI server
echo "Starting PaperLens backend server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
