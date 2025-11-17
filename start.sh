#!/bin/bash

# Quick start script for development

echo "🚀 Starting Bonus Discount Dashboard..."

# Check if backend is already running
if lsof -ti:5000 > /dev/null 2>&1; then
    echo "⚠️  Backend already running on port 5000"
else
    echo "Starting backend..."
    cd backend
    source venv/bin/activate
    nohup python api/app.py > /tmp/backend.log 2>&1 &
    cd ..
    echo "✅ Backend started on http://localhost:5000"
fi

# Check if frontend is already running
if lsof -ti:3000 > /dev/null 2>&1; then
    echo "⚠️  Frontend already running on port 3000"
else
    echo "Starting frontend..."
    cd frontend
    BROWSER=none npm start > /tmp/frontend.log 2>&1 &
    cd ..
    echo "✅ Frontend starting on http://localhost:3000"
fi

echo ""
echo "📊 Dashboard is starting..."
echo ""
echo "Backend API: http://localhost:5000/api"
echo "Frontend UI: http://localhost:3000"
echo ""
echo "To view logs:"
echo "  Backend: tail -f /tmp/backend.log"
echo "  Frontend: tail -f /tmp/frontend.log"
echo ""
echo "To stop all services: ./stop.sh"
