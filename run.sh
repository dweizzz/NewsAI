#!/bin/bash

# Function to stop all background processes on script termination
cleanup() {
    echo "Stopping servers..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup on script termination
trap cleanup SIGINT SIGTERM

# Start backend server
echo "Starting backend server..."
cd backend
uvicorn app.main:app --reload &
BACKEND_PID=$!

# Start frontend server
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 