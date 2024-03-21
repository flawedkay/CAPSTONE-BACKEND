import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from models import Region,State,LGA

# Create a test client using the TestClient class
client = TestClient(app)



@pytest.fixture
def mock_db_session():
    with patch('main.SessionLocal') as mock:
        mock.return_value = MagicMock()
        yield mock

# Define test cases for each endpoint

def test_read_all_regions(mock_db_session):
    response = client.get("/locale/region")
    mock_db_session.return_value.query.return_value.all.return_value =[Region(name="SOUTH-EAST"),Region(name="NORTH-WEST")]
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"
    assert isinstance(response.json(), list)  # Assuming the response is a list of regions

def test_read_all_State(mock_db_session):
    response = client.get("/locale/state")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"
    assert isinstance(response.json(), list)  # Assuming the response is a list of states

def test_read_states_by_region(mock_db_session):
    response = client.get("/locale/state{region_no}", params={"region_no": "some_region"})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"
    assert isinstance(response.json(), list)  # Assuming the response is a list of states

def test_read_lgas_by_state(mock_db_session):
    response = client.get("/locale/LGA{state_no}", params={"state_no": "some_state"})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"
    assert isinstance(response.json(), list)  # Assuming the response is a list of LGAs
