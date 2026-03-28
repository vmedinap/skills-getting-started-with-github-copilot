"""
Tests for signup functionality (POST /activities/{activity_name}/signup)
Using AAA (Arrange-Act-Assert) pattern
"""
import pytest


class TestSignup:
    """Test suite for signup endpoint"""

    def test_signup_new_student_success(self, client):
        """
        GIVEN: A valid activity and new student email
        WHEN: Student signs up for activity
        THEN: Signup succeeds with 200 status and confirmation message
        """
        # Arrange
        activity_name = "Basketball"
        new_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Signed up" in data["message"]
        assert new_email in data["message"]

    def test_signup_adds_student_to_participants(self, client):
        """
        GIVEN: A valid activity
        WHEN: New student signs up
        THEN: Student appears in activity's participants list
        """
        # Arrange
        activity_name = "Tennis Club"
        new_email = "testuser@mergington.edu"

        # Act
        client.post(f"/activities/{activity_name}/signup?email={new_email}")
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert new_email in activities[activity_name]["participants"]

    def test_signup_duplicate_email_fails(self, client):
        """
        GIVEN: A student already signed up for an activity
        WHEN: Same student attempts to sign up again
        THEN: Signup fails with 400 status and error message
        """
        # Arrange
        activity_name = "Basketball"
        email = "alex@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity_fails(self, client):
        """
        GIVEN: An activity that doesn't exist
        WHEN: Student attempts to sign up
        THEN: Signup fails with 404 status
        """
        # Arrange
        nonexistent_activity = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_increments_participant_count(self, client):
        """
        GIVEN: An activity with known participant count
        WHEN: New student signs up
        THEN: Participant count increases by 1
        """
        # Arrange
        activity_name = "Chess Club"
        initial_response = client.get("/activities")
        initial_count = len(
            initial_response.json()[activity_name]["participants"]
        )
        new_email = "participant@mergington.edu"

        # Act
        client.post(f"/activities/{activity_name}/signup?email={new_email}")
        updated_response = client.get("/activities")
        updated_count = len(
            updated_response.json()[activity_name]["participants"]
        )

        # Assert
        assert updated_count == initial_count + 1
