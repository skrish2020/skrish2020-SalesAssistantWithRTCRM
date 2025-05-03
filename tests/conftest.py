import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables before tests"""
    load_dotenv()

@pytest.fixture
def mock_salesforce(monkeypatch):
    """Mock Salesforce connection for testing"""
    class MockSalesforce:
        def __init__(self):
            self.query_count = 0

        def query(self, query):
            self.query_count += 1
            if "Account" in query:
                return {
                    "records": [{
                        "Id": "001000000000000",
                        "Name": "Test Account",
                        "Industry": "Technology",
                        "AnnualRevenue": 1000000,
                        "NumberOfEmployees": 50,
                        "Description": "Test account for testing purposes"
                    }]
                }
            elif "Opportunity" in query:
                return {
                    "records": [{
                        "Id": "006000000000000",
                        "Name": "Test Opportunity",
                        "StageName": "Closed Won",
                        "Amount": 50000,
                        "CloseDate": "2025-05-01",
                        "Probability": 0.9
                    }]
                }
            return {"records": []}

    monkeypatch.setattr("sales_assistant.Salesforce", MockSalesforce)
    return MockSalesforce()
