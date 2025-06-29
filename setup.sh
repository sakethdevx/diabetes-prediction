#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install pip-tools and compile requirements
pip install pip-tools
pip-compile requirements.in
pip-sync

# Create necessary directories
mkdir -p models

echo "Setup complete. Activate the virtual environment with 'source venv/bin/activate'"
