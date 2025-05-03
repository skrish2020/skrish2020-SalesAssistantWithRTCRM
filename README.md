# Sales Assistant with Real-time CRM Integration

This project demonstrates a Sales Assistant application that integrates Salesforce CRM data with LangChain and OpenAI's GPT to provide intelligent sales support.

## Features

- Real-time Salesforce CRM data integration
- AI-powered sales analysis and recommendations
- Interactive Streamlit-based dashboard
- Natural language processing capabilities
- Opportunity management insights

## Prerequisites

- Python 3.8+
- Salesforce account with API access
- OpenAI API key

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Set up and activate virtual environment:
   ```bash
   # For Windows
   .\setup.bat
   
   # For Unix/Mac
   ./setup.sh
   ```

4. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   copy .env.example .env
   ```

5. Start the application:
   ```bash
   streamlit run sales_assistant.py
   ```

## Environment Variables

Create a `.env` file with the following variables:

```
# Salesforce Credentials
SALESFORCE_USERNAME=your_salesforce_username
SALESFORCE_PASSWORD=your_salesforce_password
SALESFORCE_SECURITY_TOKEN=your_salesforce_security_token

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Enter a Salesforce Account ID in the sidebar
2. View customer information and opportunities
3. Ask questions about the customer data
4. Get AI-powered analysis and recommendations

## Project Structure

```
SalesAsstwithRtCRM/
├── sales_assistant.py      # Main application file
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md              # Project documentation
```
