"""
Pytest configuration and fixtures for the Mergington High School API tests
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, DEFAULT_ACTIVITIES, get_activities_db


@pytest.fixture
def mock_activities():
    """
    Fixture providing a fresh copy of activities data for each test.
    This ensures test isolation - one test's data changes don't affect others.
    """
    return deepcopy(DEFAULT_ACTIVITIES)


@pytest.fixture
def client(mock_activities):
    """
    Fixture providing a TestClient with isolated activities data.
    Overrides the get_activities_db dependency to use mock_activities
    for all requests in this test.
    """
    # Override the dependency for all routes
    app.dependency_overrides[get_activities_db] = lambda: mock_activities
    
    test_client = TestClient(app)
    
    # Cleanup: restore original dependency after test
    yield test_client
    
    app.dependency_overrides.clear()
