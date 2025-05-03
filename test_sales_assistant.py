from sales_assistant import get_customer_data, get_opportunities
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_sales_assistant():
    # Test account ID (Tech Solutions Inc.)
    test_account_id = "001gL000005KxU6QAK"
    
    print("\nTesting Sales Assistant with Tech Solutions Inc. account...")
    
    # Test getting customer data
    print("\nFetching customer data...")
    customer_data = get_customer_data(test_account_id)
    if customer_data:
        print("\nCustomer Data:")
        print(f"Name: {customer_data.get('Name', 'N/A')}")
        print(f"Industry: {customer_data.get('Industry', 'N/A')}")
        print(f"Annual Revenue: ${customer_data.get('AnnualRevenue', 0):,}")
        print(f"Employees: {customer_data.get('NumberOfEmployees', 0)}")
        print(f"Description: {customer_data.get('Description', 'N/A')}")
    else:
        print("Failed to fetch customer data")
    
    # Test getting opportunities
    print("\nFetching opportunities...")
    opportunities = get_opportunities(test_account_id)
    if opportunities:
        print("\nOpportunities:")
        for opp in opportunities:
            print(f"\nOpportunity Name: {opp.get('Name', 'N/A')}")
            print(f"Stage: {opp.get('StageName', 'N/A')}")
            print(f"Amount: ${opp.get('Amount', 0):,}")
            print(f"Close Date: {opp.get('CloseDate', 'N/A')}")
            print(f"Probability: {opp.get('Probability', 0)}%")
    else:
        print("Failed to fetch opportunities")

if __name__ == "__main__":
    test_sales_assistant()
