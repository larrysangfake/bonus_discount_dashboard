#!/bin/bash

# Stop all services

echo "🛑 Stopping Bonus Discount Dashboard..."

# Kill backend
if lsof -ti:5000 > /dev/null 2>&1; then
    echo "Stopping backend..."
    lsof -ti:5000 | xargs kill
    pkill -f "python.*api/app.py"
    echo "✅ Backend stopped"
else
    echo "Backend not running"
fi

# Kill frontend
if lsof -ti:3000 > /dev/null 2>&1; then
    echo "Stopping frontend..."
    lsof -ti:3000 | xargs kill
    pkill -f "react-scripts"
    echo "✅ Frontend stopped"
else
    echo "Frontend not running"
fi

echo ""
echo "All services stopped."
