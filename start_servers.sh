#!/bin/bash

echo "=========================================="
echo "🚀 Starting Kambel Consult Servers"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Running setup..."
    bash setup.sh
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if Django database is set up
if [ ! -f "django_admin/db.sqlite3" ]; then
    echo "Setting up Django database..."
    cd django_admin
    python3 manage.py migrate
    cd ..
fi

echo ""
echo "=========================================="
echo "Starting servers..."
echo "=========================================="
echo ""
echo "📍 Frontend: http://localhost:5001"
echo "📍 Backend API: http://localhost:8000"
echo "📍 Django Admin: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Start Django server in background
cd django_admin
python3 manage.py runserver 8000 &
DJANGO_PID=$!
cd ..

# Wait a moment for Django to start
sleep 2

# Start Flask server in foreground
python3 app.py &
FLASK_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $DJANGO_PID 2>/dev/null
    kill $FLASK_PID 2>/dev/null
    echo "Servers stopped."
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Wait for both processes
wait $FLASK_PID

