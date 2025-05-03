import pytest
from sales_assistant import get_customer_data, get_opportunities

# Use the mock_salesforce fixture from conftest.py

def test_get_customer_data(mock_salesforce):
    """Test getting customer data"""
    customer = get_customer_data("001000000000000")
    assert customer is not None
    assert customer["Name"] == "Test Account"
    assert customer["Industry"] == "Technology"
    assert customer["AnnualRevenue"] == 1000000
    assert customer["NumberOfEmployees"] == 50
    assert customer["Description"] == "Test account for testing purposes"

def test_get_opportunities(mock_salesforce):
    """Test getting opportunities"""
    opps = get_opportunities("001000000000000")
    assert len(opps) == 1
    assert opps[0]["Name"] == "Test Opportunity"
    assert opps[0]["StageName"] == "Closed Won"
    assert opps[0]["Amount"] == 50000
    assert opps[0]["CloseDate"] == "2025-05-01"
    assert opps[0]["Probability"] == 0.9

def test_get_customer_data_nonexistent(mock_salesforce):
    """Test getting non-existent customer"""
    customer = get_customer_data("nonexistent")
    assert customer is None

def test_get_opportunities_nonexistent(mock_salesforce):
    """Test getting opportunities for non-existent account"""
    opps = get_opportunities("nonexistent")
    assert len(opps) == 0

def test_get_customer_data(mock_salesforce):
    """Test getting customer data"""
    customer = get_customer_data("001000000000000")
    assert customer is not None
    assert customer["Name"] == "Test Account"
    assert customer["Industry"] == "Technology"
    assert customer["AnnualRevenue"] == 1000000
    assert customer["NumberOfEmployees"] == 50

def test_get_opportunities(mock_salesforce):
    """Test getting opportunities"""
    opps = get_opportunities("001000000000000")
    assert len(opps) == 1
    assert opps[0]["Name"] == "Test Opportunity"
    assert opps[0]["StageName"] == "Closed Won"
    assert opps[0]["Amount"] == 50000
    assert opps[0]["Probability"] == 0.9

def test_get_customer_data_nonexistent(mock_salesforce):
    """Test getting non-existent customer"""
    mock_salesforce.query.return_value = {"records": []}
    customer = get_customer_data("nonexistent")
    assert customer is None

def test_get_opportunities_nonexistent(mock_salesforce):
    """Test getting opportunities for non-existent account"""
    mock_salesforce.query.return_value = {"records": []}
    opps = get_opportunities("nonexistent")
    assert len(opps) == 0
