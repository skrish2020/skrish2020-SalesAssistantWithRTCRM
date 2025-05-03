@echo off

echo Running tests...
pytest -v --cov=sales_assistant --cov-report=term-missing

if errorlevel 1 (
    echo Tests failed. Exiting...
    exit /b 1
)

echo Running linters...
black .
isort .
flake8 .

if errorlevel 1 (
    echo Linting failed. Exiting...
    exit /b 1
)

echo Starting application...
streamlit run sales_assistant.py
