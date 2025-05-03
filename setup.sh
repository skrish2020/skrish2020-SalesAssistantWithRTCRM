#!/bin/bash

# Activate virtual environment
echo "Activating virtual environment..."
source windusurf_python_SF_env/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check installation
echo "Checking installation..."
pip list

echo "Setup complete! You can now run the application with:"
echo "streamlit run sales_assistant.py"
