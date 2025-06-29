#!/bin/bash
set -e  # Exit on error

echo "🚀 Setting up Diabetes Prediction App..."

# Create virtual environment
echo "🔧 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "🔄 Upgrading pip..."
python -m pip install --upgrade pip

# Install pip-tools and compile requirements
echo "📦 Installing pip-tools and compiling requirements..."
pip install pip-tools
pip-compile requirements.in
pip-sync

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements-deploy.txt

# Create necessary directories
echo "📁 Creating required directories..."
mkdir -p models

echo "✅ Setup completed successfully!"
echo "To run the app, use: streamlit run app.py"
echo "Setup complete. Activate the virtual environment with 'source venv/bin/activate'"
