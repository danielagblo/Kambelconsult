#!/bin/bash

echo "=========================================="
echo "Kambel Consult - Project Setup"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Django requirements
echo ""
echo "Installing Django dependencies..."
cd django_admin
pip install -r requirements.txt
cd ..

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p data
mkdir -p static/uploads
mkdir -p django_admin/media
mkdir -p django_admin/static

# Set up Django database
echo ""
echo "Setting up Django database..."
cd django_admin
python3 manage.py migrate
cd ..

# Create Django superuser (optional)
echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment in the future:"
echo "  source .venv/bin/activate"
echo ""
echo "To start the development server:"
echo "  python3 app.py"
echo ""
echo "To access Django admin panel:"
echo "  cd django_admin && python3 manage.py runserver 8000"
echo "  Then visit: http://localhost:8000/admin"
echo ""
echo "To create a Django superuser (optional):"
echo "  cd django_admin && python3 manage.py createsuperuser"
echo ""

