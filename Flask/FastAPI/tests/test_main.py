from fastapi.testclient import TestClient
from FastAPI.main import app
from FastAPI.database import get_db
import pytest
from unittest.mock import Mock
from Flask.FastAPI.auth.security import oauth2_scheme


# Mock dependencies
mock_session = Mock()   #mocks get_db
#also mock token dependency

def get_mock_session():
    yield mock_session

app.dependency_overrides[get_db] = get_mock_session()
app.dependency_overrides[oauth2_scheme] = Mock(return_value="fake_access_token")


@pytest.fixture
def fake_session():
    #create session for each test, then teardown after each test ?????
    return mock_session
#terminates after all tests done

@pytest.fixture
def test_client():
    return TestClient(app)


def test_root():
    response = test_client().get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_upload_image_without_file(test_client):
    response = test_client.post("/upload")
    assert response.status_code == 422  # Unprocessable Entity