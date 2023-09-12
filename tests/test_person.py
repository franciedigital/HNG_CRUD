import pytest
import requests

# Define the base URL for your API
BASE_URL = 'http://localhost:8000'

@pytest.fixture
def sample_person():
    # Define a sample person data for testing
    return {
        'name': 'Mark Essien'
    }

def test_create_person(sample_person):
    # Test creating a new person
    response = requests.post(f'{BASE_URL}/api', json=sample_person)
    assert response.status_code == 200

def test_get_person():
    # Test fetching details of a person
    response = requests.get(f'{BASE_URL}/api/user_id?name=Mark%20Essien')
    assert response.status_code == 200

def test_update_person(sample_person):
    # Test modifying the details of an existing person
    updated_data = {'name': 'John Essien'}
    response = requests.put(f'{BASE_URL}/api/user_id?name=Mark%20Essien', json=updated_data)
    assert response.status_code == 200

def test_delete_person():
    # Test removing a person
    response = requests.delete(f'{BASE_URL}/api/user_id?name=John%20Essien')
    assert response.status_code == 200
