"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern
"""

import pytest


class TestSignup:
    """Test cases for signing up students for activities"""
    
    def test_signup_successful(self, client, mock_activities):
        """
        Arrange: Empty Soccer Club activity
        Act: Sign up a new student
        Assert: Student is added to participant list
        """
        # Arrange
        activity_name = "Soccer Club"
        email = "alice@mergington.edu"
        initial_count = len(mock_activities[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert len(mock_activities[activity_name]["participants"]) == initial_count + 1
        assert email in mock_activities[activity_name]["participants"]
    
    def test_signup_duplicate_email_fails(self, client, mock_activities):
        """
        Arrange: Student already signed up for Chess Club
        Act: Try to sign up same student again
        Assert: Request fails with 400 error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_fails(self, client):
        """
        Arrange: Nonexistent activity name
        Act: Try to sign up for unknown activity
        Assert: Request fails with 404 error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "bob@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_returns_success_message(self, client):
        """
        Arrange: Valid signup request
        Act: Sign up for activity
        Assert: Response contains meaningful success message
        """
        # Arrange
        activity_name = "Art Club"
        email = "charlie@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]
