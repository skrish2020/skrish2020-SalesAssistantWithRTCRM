import streamlit as st
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from simple_salesforce import Salesforce
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sales_assistant.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

# Initialize Salesforce connection
sf = Salesforce(
    username=os.getenv('SALESFORCE_USERNAME'),
    password=os.getenv('SALESFORCE_PASSWORD'),
    security_token=os.getenv('SALESFORCE_SECURITY_TOKEN')
)

# Initialize OpenAI LLM
llm = OpenAI(
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    temperature=0.7
)

def get_customer_data(account_id):
    """Fetch customer data from Salesforce"""
    try:
        query = f"SELECT Name, Industry, AnnualRevenue, NumberOfEmployees, Description, CreatedDate FROM Account WHERE Id = '{account_id}'"
        result = sf.query(query)
        if result['records']:
            return result['records'][0]
        else:
            logging.warning(f"No customer found for Account ID: {account_id}")
            return None
    except Exception as e:
        logging.error(f"Error fetching customer data: {str(e)}")
        st.error(f"Error fetching customer data: {str(e)}")
        return None

def get_opportunities(account_id):
    """Fetch opportunities for a specific account"""
    try:
        query = f"SELECT Id, Name, StageName, Amount, CloseDate, Probability FROM Opportunity WHERE AccountId = '{account_id}'"
        result = sf.query(query)
        return result['records']
    except Exception as e:
        logging.error(f"Error fetching opportunities: {str(e)}")
        st.error(f"Error fetching opportunities: {str(e)}")
        return []

def main():
    try:
        st.title("Sales Assistant")
        
        # Sidebar for configuration
        st.sidebar.header("Configuration")
        account_id = st.sidebar.text_input("Enter Account ID:")
        
        if account_id:
            # Get customer data
            customer_data = get_customer_data(account_id)
            if customer_data:
                st.subheader("Customer Information")
                customer_info = {
                    "Name": customer_data.get('Name', ''),
                    "Industry": customer_data.get('Industry', ''),
                    "Annual Revenue": customer_data.get('AnnualRevenue', ''),
                    "Employees": customer_data.get('NumberOfEmployees', ''),
                    "Description": customer_data.get('Description', '')
                }
                st.json(customer_info)
                
                # Get opportunities
                opportunities = get_opportunities(account_id)
                if opportunities:
                    st.subheader("Active Opportunities")
                    opp_data = []
                    for opp in opportunities:
                        opp_data.append({
                            "Name": opp.get('Name', ''),
                            "Stage": opp.get('StageName', ''),
                            "Amount": opp.get('Amount', ''),
                            "Close Date": opp.get('CloseDate', ''),
                            "Probability": opp.get('Probability', '')
                        })
                    st.json(opp_data)
                
                # Chat interface
                st.subheader("Ask the Sales Assistant")
                user_input = st.text_area("Your question:", height=100)
                
                if user_input:
                    # Create a prompt template
                    template = """You are a sales assistant helping analyze customer data and opportunities.
                    Customer Data: {customer_data}
                    Opportunities: {opportunities}
                    
                    Question: {question}
                    
                    Please provide a detailed analysis and recommendations.
                    
                    Format your response in markdown with clear sections:
                    1. Analysis of customer data
                    2. Opportunity assessment
                    3. Strategic recommendations
                    4. Actionable next steps
                    """
                    
                    prompt = PromptTemplate(
                        input_variables=["customer_data", "opportunities", "question"],
                        template=template
                    )
                    
                    chain = LLMChain(llm=llm, prompt=prompt)
                    
                    # Format data for the prompt
                    customer_str = str(customer_data)
                    opportunities_str = str(opportunities)
                    
                    # Get response
                    response = chain.run(
                        customer_data=customer_str,
                        opportunities=opportunities_str,
                        question=user_input
                    )
                    
                    st.subheader("Assistant's Response")
                    st.markdown(response)
            else:
                st.error("Account not found. Please check the Account ID.")
                
    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
