from simple_salesforce import Salesforce
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Salesforce connection
sf = Salesforce(
    username=os.getenv('SALESFORCE_USERNAME'),
    password=os.getenv('SALESFORCE_PASSWORD'),
    security_token=os.getenv('SALESFORCE_SECURITY_TOKEN')
)

import random
import string

def generate_random_string(length):
    """Generate a random string of specified length"""
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_phone():
    """Generate a random phone number in format 555-XXX-XXXX"""
    return f"555-{random.randint(100,999)}-{random.randint(1000,9999)}"

def generate_random_website(name):
    """Generate a random website URL based on company name"""
    return f"www.{name.lower().replace(' ', '')}.com"

def create_sample_accounts():
    """Create 100 diverse sample account records with random data"""
    # Define country and state codes that Salesforce recognizes
    COUNTRY_CODES = {
        'US': 'United States',
        'GB': 'United Kingdom',
        'DE': 'Germany',
        'FR': 'France',
        'JP': 'Japan',
        'AU': 'Australia'
    }
    
    STATE_CODES = {
        'CA': 'California',
        'NY': 'New York',
        'TX': 'Texas',
        'CO': 'Colorado',
        'WA': 'Washington',
        'MA': 'Massachusetts',
        'IL': 'Illinois',
        'FL': 'Florida',
        'PA': 'Pennsylvania',
        'NJ': 'New Jersey'
    }
    
    # List of industries
    INDUSTRIES = [
        'Technology', 'Healthcare', 'Retail', 'Energy', 'Food & Beverage',
        'Education', 'Manufacturing', 'Finance', 'Transportation', 'Construction',
        'Telecommunications', 'Pharmaceuticals', 'Automotive', 'Aerospace',
        'Real Estate', 'Legal', 'Consulting', 'Media', 'Entertainment',
        'Hospitality', 'Mining', 'Utilities', 'Agriculture', 'Insurance'
    ]
    
    # List of cities
    CITIES = [
        'San Francisco', 'New York', 'Los Angeles', 'Chicago', 'Houston',
        'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas',
        'Seattle', 'Denver', 'Boston', 'Atlanta', 'Portland',
        'Miami', 'Washington DC', 'Baltimore', 'Sacramento', 'Austin'
    ]
    
    created_accounts = []
    
    for i in range(100):
        # Generate random account data
        industry = random.choice(INDUSTRIES)
        name = f"{industry} {generate_random_string(3)} {random.randint(1, 100)}"
        
        # Generate random revenue and employees
        if industry in ['Technology', 'Healthcare', 'Finance']:
            annual_revenue = random.randint(1000000, 10000000)
            employees = random.randint(50, 500)
        else:
            annual_revenue = random.randint(500000, 5000000)
            employees = random.randint(20, 200)
        
        # Generate random description
        descriptions = [
            "Leading provider of innovative solutions",
            "Fast-growing company with global presence",
            "Customer-focused organization with cutting-edge technology",
            "Industry leader with strong market position",
            "Sustainable business practices and growth"
        ]
        description = f"{random.choice(descriptions)} in the {industry} industry"
        
        # Generate random location
        country = random.choice(list(COUNTRY_CODES.keys()))
        if country == 'US':
            state = random.choice(list(STATE_CODES.keys()))
            city = random.choice(CITIES)
        else:
            state = ''
            city = ''
        
        account = {
            'Name': name,
            'Industry': industry,
            'AnnualRevenue': annual_revenue,
            'NumberOfEmployees': employees,
            'Description': description,
            'Phone': generate_random_phone(),
            'Website': generate_random_website(name),
            'BillingStreet': f"{random.randint(100, 999)} {random.choice(['Street', 'Avenue', 'Road', 'Drive'])}",
            'BillingCity': city,
            'BillingState': STATE_CODES[state] if state else '',
            'BillingPostalCode': str(random.randint(10000, 99999)),
            'BillingCountry': COUNTRY_CODES[country]
        }
        
        try:
            # Check if account already exists
            query = f"SELECT Id FROM Account WHERE Name = '{name}'"
            result = sf.query(query)
            if result['records']:
                existing_id = result['records'][0]['Id']
                print(f"Account {name} already exists with ID: {existing_id}")
                created_accounts.append(existing_id)
                continue
            
            # Create new account if it doesn't exist
            result = sf.Account.create(account)
            print(f"Successfully created Account: {name} with ID: {result['id']}")
            created_accounts.append(result['id'])
        except Exception as e:
            print(f"Error creating account {name}: {str(e)}")
    
    return created_accounts

def delete_duplicate_accounts():
    """Delete duplicate accounts based on name"""
    try:
        # Get all accounts
        query = "SELECT Id, Name FROM Account"
        result = sf.query(query)
        accounts = result['records']
        
        # Create a dictionary to track account names and their IDs
        account_dict = {}
        duplicates = []
        
        for account in accounts:
            name = account['Name']
            if name in account_dict:
                # If name already exists, mark as duplicate
                duplicates.append(account['Id'])
            else:
                account_dict[name] = account['Id']
        
        # Delete duplicate accounts
        for dup_id in duplicates:
            try:
                # First delete associated opportunities
                query = f"SELECT Id FROM Opportunity WHERE AccountId = '{dup_id}'"
                opp_result = sf.query(query)
                for opp in opp_result['records']:
                    try:
                        sf.Opportunity.delete(opp['Id'])
                        print(f"Deleted opportunity {opp['Id']} for account {dup_id}")
                    except Exception as e:
                        print(f"Error deleting opportunity {opp['Id']}: {str(e)}")
                
                # Then delete the account
                sf.Account.delete(dup_id)
                print(f"Deleted duplicate account with ID: {dup_id}")
            except Exception as e:
                print(f"Error deleting account {dup_id}: {str(e)}")
        
        if not duplicates:
            print("No duplicate accounts found")
            
    except Exception as e:
        print(f"Error in delete_duplicate_accounts: {str(e)}")

def create_sample_opportunities(account_ids):
    """Create sample opportunities for multiple accounts"""
    STAGE_NAMES = [
        'Prospecting',
        'Qualification',
        'Needs Analysis',
        'Value Proposition',
        'Id. Decision Makers',
        'Perception Analysis',
        'Proposal/Price Quote',
        'Negotiation/Review',
        'Closed Won',
        'Closed Lost'
    ]
    
    # Fetch account details for each account ID
    accounts = {}
    for account_id in account_ids:
        try:
            account = sf.Account.get(account_id)
            accounts[account_id] = account
        except Exception as e:
            print(f"Error fetching account {account_id}: {str(e)}")
            continue
    
    for account_id in account_ids:
        account = accounts.get(account_id, {'Name': 'Unknown'})
        opportunities = [
            {
                'Name': f'{account_id} - {account.get("Name", "Unknown")} - New Product Implementation',
                'StageName': STAGE_NAMES[3],  # Value Proposition
                'CloseDate': '2025-07-01',
                'Amount': 150000,
                'Probability': 70,
                'AccountId': account_id
            },
            {
                'Name': f'{account_id} - {account.get("Name", "Unknown")} - Enterprise Upgrade',
                'StageName': STAGE_NAMES[6],  # Proposal/Price Quote
                'CloseDate': '2025-08-15',
                'Amount': 250000,
                'Probability': 85,
                'AccountId': account_id
            },
            {
                'Name': f'{account_id} - {account.get("Name", "Unknown")} - Support Contract',
                'StageName': STAGE_NAMES[7],  # Negotiation/Review
                'CloseDate': '2025-09-01',
                'Amount': 50000,
                'Probability': 90,
                'AccountId': account_id
            },
            {
                'Name': f'{account_id} - {account.get("Name", "Unknown")} - Training Program',
                'StageName': STAGE_NAMES[4],  # Needs Analysis
                'CloseDate': '2025-07-15',
                'Amount': 75000,
                'Probability': 60,
                'AccountId': account_id
            },
            {
                'Name': f'{account_id} - {account.get("Name", "Unknown")} - Integration Project',
                'StageName': STAGE_NAMES[5],  # Value Proposition
                'CloseDate': '2025-08-01',
                'Amount': 200000,
                'Probability': 75,
                'AccountId': account_id
            }
        ]
        
        for opp in opportunities:
            try:
                result = sf.Opportunity.create(opp)
                print(f"Created Opportunity: {opp['Name']} with ID: {result['id']}")
            except Exception as e:
                print(f"Error creating opportunity for account {account_id}: {str(e)}")

def main():
    # First delete any duplicate accounts
    delete_duplicate_accounts()
    
    # Then create sample accounts and opportunities
    account_ids = create_sample_accounts()
    if account_ids:
        # Save account IDs to a file
        with open('account_ids.txt', 'w') as f:
            for account_id in account_ids:
                f.write(f"{account_id}\n")
        print(f"\nSaved {len(account_ids)} account IDs to account_ids.txt")
        
        create_sample_opportunities(account_ids)

if __name__ == "__main__":
    main()
