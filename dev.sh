#!/bin/bash

# Run tests
echo "Running tests..."
pytest -v --cov=sales_assistant --cov-report=term-missing

# Run linters
echo "Running linters..."
black .
isort .
flake8 .

# Run type checking
echo "Running type checking..."
mypy .

# Run the application
echo "Starting application..."
streamlit run sales_assistant.py
