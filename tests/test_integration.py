import pytest
import os
from dotenv import load_dotenv
from sales_assistant import main

@pytest.fixture
def mock_streamlit(monkeypatch):
    """Mock Streamlit functions for testing"""
    class MockSt:
        def __init__(self):
            self.title_called = False
            self.subheader_called = False
            self.text_input_called = False
            self.error_called = False
            self.write_called = False
            self.json_called = False
            self.text_area_called = False
            self.markdown_called = False

        def title(self, text):
            self.title_called = True
            assert text == "Sales Assistant"

        def subheader(self, text):
            self.subheader_called = True

        def text_input(self, label):
            self.text_input_called = True
            return "001000000000000"

        def text_area(self, label, height):
            self.text_area_called = True
            return "What are the key opportunities for this account?"

        def error(self, message):
            self.error_called = True

        def write(self, content):
            self.write_called = True

        def json(self, data):
            self.json_called = True

        def markdown(self, content):
            self.markdown_called = True

    monkeypatch.setattr("sales_assistant.st", MockSt())
    return MockSt()

@pytest.fixture
def mock_salesforce_integration(monkeypatch):
    """Mock Salesforce integration for testing"""
    class MockSalesforceIntegration:
        def __init__(self):
            self.query_count = 0

        def get_customer_data(self, account_id):
            self.query_count += 1
            return {
                "Id": account_id,
                "Name": "Test Account",
                "Industry": "Technology",
                "AnnualRevenue": 1000000,
                "NumberOfEmployees": 50,
                "Description": "Test account for testing purposes"
            }

        def get_opportunities(self, account_id):
            self.query_count += 1
            return [{
                "Id": "006000000000000",
                "Name": "Test Opportunity",
                "StageName": "Closed Won",
                "Amount": 50000,
                "CloseDate": "2025-05-01",
                "Probability": 0.9
            }]

    monkeypatch.setattr("sales_assistant.Salesforce", MockSalesforceIntegration)
    return MockSalesforceIntegration()

@pytest.fixture
def mock_llm(monkeypatch):
    """Mock LLM for testing"""
    class MockLLM:
        def __init__(self):
            self.run_count = 0

        def run(self, **kwargs):
            self.run_count += 1
            return """## Analysis of Customer Data
- Industry: Technology
- Revenue: $1M
- Employees: 50

## Opportunity Assessment
- Key Opportunity: Test Opportunity
- Status: Closed Won
- Value: $50K
- Probability: 90%

## Strategic Recommendations
1. Focus on upselling additional services
2. Explore cross-selling opportunities
3. Schedule regular check-ins

## Actionable Next Steps
1. Review contract renewal dates
2. Schedule QBR
3. Prepare case studies"""

    monkeypatch.setattr("sales_assistant.LLMChain", MockLLM)
    return MockLLM()

def test_main_integration(mock_streamlit, mock_salesforce_integration, mock_llm):
    """Test main application integration"""
    main()
    
    # Verify Streamlit interactions
    assert mock_streamlit.title_called
    assert mock_streamlit.subheader_called
    assert mock_streamlit.text_input_called
    assert mock_streamlit.text_area_called
    assert mock_streamlit.json_called
    assert mock_streamlit.markdown_called
    
    # Verify Salesforce interactions
    assert mock_salesforce_integration.query_count == 2
    
    # Verify LLM interactions
    assert mock_llm.run_count == 1

def test_error_handling(mock_streamlit, monkeypatch):
    """Test error handling"""
    class MockSalesforceError:
        def __init__(self):
            pass

        def get_customer_data(self, account_id):
            raise Exception("Test error")

    monkeypatch.setattr("sales_assistant.Salesforce", MockSalesforceError)
    main()
    
    assert mock_streamlit.error_called
