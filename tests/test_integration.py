"""
Integration tests combining multiple operations
Using AAA (Arrange-Act-Assert) pattern
"""
import pytest


class TestIntegration:
    """Integration test suite combining multiple operations"""

    def test_signup_and_unregister_workflow(self, client):
        """
        GIVEN: An activity with initial state
        WHEN: Student signs up then immediately unregisters
        THEN: Activity returns to initial participant count
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "workflow@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(
            initial_response.json()[activity_name]["participants"]
        )

        # Act - Signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        assert signup_response.status_code == 200

        # Assert - After signup
        mid_response = client.get("/activities")
        mid_count = len(
            mid_response.json()[activity_name]["participants"]
        )
        assert mid_count == initial_count + 1

        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        assert unregister_response.status_code == 200

        # Assert - After unregister
        final_response = client.get("/activities")
        final_count = len(
            final_response.json()[activity_name]["participants"]
        )
        assert final_count == initial_count

    def test_multiple_students_signup_sequence(self, client):
        """
        GIVEN: An activity
        WHEN: Multiple students sign up in sequence
        THEN: All participants are recorded correctly
        """
        # Arrange
        activity_name = "Basketball"
        students = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu",
        ]
        initial_response = client.get("/activities")
        initial_count = len(
            initial_response.json()[activity_name]["participants"]
        )

        # Act - Sign up all students
        for email in students:
            response = client.post(
                f"/activities/{activity_name}/signup?email={email}"
            )
            assert response.status_code == 200

        # Assert - All students added
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity_name]["participants"]
        assert len(final_participants) == initial_count + len(students)
        for email in students:
            assert email in final_participants

    def test_signup_after_unregister_succeeds(self, client):
        """
        GIVEN: A student who unregistered from an activity
        WHEN: Same student attempts to sign up again
        THEN: Signup succeeds (can re-register after unregistering)
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act - Unregister first
        client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Act - Try to sign up again
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert - Signup succeeds
        assert response.status_code == 200
        final_response = client.get("/activities")
        assert email in final_response.json()[activity_name]["participants"]
