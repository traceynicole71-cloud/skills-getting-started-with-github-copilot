"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestGetActivities:
    """Test cases for retrieving all activities"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Create a client with default activities
        Act: Make GET request to /activities
        Assert: Verify all activities are returned with correct structure
        """
        # Arrange
        expected_activity_count = 9
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == expected_activity_count
        assert "Chess Club" in data
        assert "Programming Class" in data
    
    def test_get_activities_returns_activity_details(self, client):
        """
        Arrange: Activities with known structure
        Act: Get activities and inspect one activity
        Assert: Verify activity has required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        # Assert
        assert response.status_code == 200
        for field in required_fields:
            assert field in chess_club
    
    def test_get_activities_returns_current_participants(self, client):
        """
        Arrange: Activities with known participants
        Act: Get activities
        Assert: Verify participant lists are accurate
        """
        # Arrange
        # Chess Club has 2 participants by default
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(activities["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
