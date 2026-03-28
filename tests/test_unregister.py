"""
Tests for unregister functionality (DELETE /activities/{activity_name}/unregister)
Using AAA (Arrange-Act-Assert) pattern
"""
import pytest


class TestUnregister:
    """Test suite for unregister endpoint"""

    def test_unregister_registered_student_success(self, client):
        """
        GIVEN: A student registered for an activity
        WHEN: Student unregisters
        THEN: Unregister succeeds with 200 status and confirmation message
        """
        # Arrange
        activity_name = "Basketball"
        email = "alex@mergington.edu"  # Already registered

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]

    def test_unregister_removes_from_participants(self, client):
        """
        GIVEN: A registered student
        WHEN: Student unregisters
        THEN: Student is removed from activity's participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email not in activities[activity_name]["participants"]

    def test_unregister_not_registered_fails(self, client):
        """
        GIVEN: A student not registered for an activity
        WHEN: Attempt to unregister
        THEN: Request fails with 404 status
        """
        # Arrange
        activity_name = "Basketball"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not registered" in data["detail"]

    def test_unregister_nonexistent_activity_fails(self, client):
        """
        GIVEN: An activity that doesn't exist
        WHEN: Attempt to unregister from it
        THEN: Request fails with 404 status
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_decrements_participant_count(self, client):
        """
        GIVEN: An activity with multiple participants
        WHEN: One student unregisters
        THEN: Participant count decreases by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(
            initial_response.json()[activity_name]["participants"]
        )

        # Act
        client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        updated_response = client.get("/activities")
        updated_count = len(
            updated_response.json()[activity_name]["participants"]
        )

        # Assert
        assert updated_count == initial_count - 1
