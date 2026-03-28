"""
Tests for retrieving activities (GET /activities)
Using AAA (Arrange-Act-Assert) pattern
"""
import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_all_activities_returns_success(self, client):
        """
        GIVEN: An initialized app with activities
        WHEN: Client requests all activities
        THEN: Response status is 200 and contains activity data
        """
        # Arrange: Already set up by reset_activities fixture

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) >= 3

    def test_get_activities_contains_expected_activities(self, client):
        """
        GIVEN: An initialized app with predefined activities
        WHEN: Client requests all activities
        THEN: Response includes Basketball, Tennis Club, and Chess Club
        """
        # Arrange: (no additional setup needed)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert "Basketball" in activities
        assert "Tennis Club" in activities
        assert "Chess Club" in activities

    def test_get_activities_includes_participant_list(self, client):
        """
        GIVEN: An initialized app
        WHEN: Client requests all activities
        THEN: Each activity includes participants list
        """
        # Arrange: (no additional setup needed)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
