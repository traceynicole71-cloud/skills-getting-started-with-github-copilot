"""
Tests for DELETE /activities/{activity_name}/signup endpoint using AAA pattern
"""

import pytest


class TestUnregister:
    """Test cases for unregistering students from activities"""
    
    def test_unregister_successful(self, client, mock_activities):
        """
        Arrange: Student signed up for Chess Club
        Act: Unregister the student
        Assert: Student is removed from participant list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(mock_activities[activity_name]["participants"])
        assert email in mock_activities[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert len(mock_activities[activity_name]["participants"]) == initial_count - 1
        assert email not in mock_activities[activity_name]["participants"]
    
    def test_unregister_not_signed_up_fails(self, client):
        """
        Arrange: Student not signed up for Drama Club
        Act: Try to unregister
        Assert: Request fails with 400 error
        """
        # Arrange
        activity_name = "Drama Club"
        email = "david@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()
    
    def test_unregister_nonexistent_activity_fails(self, client):
        """
        Arrange: Nonexistent activity
        Act: Try to unregister from unknown activity
        Assert: Request fails with 404 error
        """
        # Arrange
        activity_name = "Unknown Club"
        email = "eve@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_returns_success_message(self, client):
        """
        Arrange: Student signed up for Programming Class
        Act: Unregister the student
        Assert: Response contains meaningful success message
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]
