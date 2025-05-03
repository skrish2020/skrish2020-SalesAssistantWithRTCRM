@echo off

echo Activating virtual environment...
call windusurf_python_SF_env\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Checking installation...
pip list

echo Setup complete! You can now run the application with:
echo streamlit run sales_assistant.py
