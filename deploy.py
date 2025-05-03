import os
import streamlit as st

# Check if running on Streamlit Cloud
if 'STREAMLIT_APP_ID' in os.environ:
    # Get environment variables from Streamlit Cloud
    SALESFORCE_USERNAME = os.environ.get('SALESFORCE_USERNAME')
    SALESFORCE_PASSWORD = os.environ.get('SALESFORCE_PASSWORD')
    SALESFORCE_SECURITY_TOKEN = os.environ.get('SALESFORCE_SECURITY_TOKEN')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Set environment variables for the app
    os.environ['SALESFORCE_USERNAME'] = SALESFORCE_USERNAME
    os.environ['SALESFORCE_PASSWORD'] = SALESFORCE_PASSWORD
    os.environ['SALESFORCE_SECURITY_TOKEN'] = SALESFORCE_SECURITY_TOKEN
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

    # Run the main application
    from sales_assistant import main
    main()
else:
    # Local development
    from sales_assistant import main
    main()
