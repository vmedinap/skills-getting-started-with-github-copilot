"""
Pytest fixtures and configuration for activity signup tests
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


# Initial test data
INITIAL_ACTIVITIES = {
    "Basketball": {
        "description": "Team sport and competitive basketball games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis skills training and friendly matches",
        "schedule": "Tuesdays and Thursdays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["jordan@mergington.edu"]
    },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
}


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities database before and after each test (Arrange phase)"""
    # Setup: Clear and reset activities to initial state
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    
    yield
    
    # Cleanup: Reset after test
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
