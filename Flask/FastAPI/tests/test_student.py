import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
# from src import app, schemas, models
from sqlalchemy.orm import Session
from datetime import datetime

from Flask.FastAPI import models
from Flask.FastAPI.main import app
from Flask.FastAPI.tests.test_main import mock_session


@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def mock_course():
    return models.Course(course_id=1, name="Test Course", number_of_students=3)

@pytest.fixture
def mock_student():
    return {
        "id": 1,
        "name": "abcd",
        "email": "abcd234@gmail.com",
        "avg_marks": "50",
        "course_id": 1
    }

student1 = {
    "name": "xyz",
    "email": "xyz123@gmail.com",
    "avg_marks": "90",
    "course_id": 1
}
student2 = {
    "name": "xzfdk",
    "avg_marks": "58.4",
    "course_id": 2
}
student3 = {
    "name": "xzdfdk",
    "email": "xyz13@gmail.com",
    "avg_marks": "58",
    "course_id": 999
}


@pytest.mark.parametrize("student_data, expected_status, expected_detail", [
    (student1, 200, None),
    (student2, 200, None),  # Assuming c_id 2 exists
    (student3, 400, "Course ID does not exist"),  # c_id 999 does not exist
])
def test_create_student(test_client, mock_course, student_data, expected_status, expected_detail):
    # Setup mocks
    mock_session.query().filter().first.return_value = mock_course  # Simulate finding the course
    mock_session.add = Mock()  # Mock the add method
    mock_session.commit = Mock()  # Mock the commit method
    mock_session.refresh = Mock()  # Mock the refresh method

    # Perform the request
    response = test_client.post("/students/create", json=student_data)

    # Check response
    assert response.status_code == expected_status
    if expected_detail:
        assert response.json()["detail"] == expected_detail
    else:
        assert response.json()["name"] == student_data["name"]
        assert mock_session.add.call_count == 1  # Ensure the student was added
        assert mock_course.number_of_students == 2  # Ensure student count was updated



def test_update_student(test_client, mock_student, mock_course):
    # Setup mocks
    mock_session.query().filter().first.return_value = mock_student
    mock_session.query(models.Course).filter().first.side_effect = [mock_course, mock_course]

    update_data = {
        "name": "abcd",
        "email": "abcd@gmail.com",
        "avg_marks": 50,
        "course_id": 1
    }

    response = test_client.put("/students/update?id=1", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "abcd"
    assert response.json()["email"] == "abcd@gmail.com"

    mock_session.query().filter().first.return_value = None  # Simulate student not found

    update_data = {
        "name": "pru fib"
    }
    response = test_client.put("/students/update?id=1", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_delete_student(test_client, mock_student, mock_course):
    # Setup mocks
    mock_session.query().filter().first.return_value = mock_student
    mock_session.query(models.Course).filter().first.return_value = mock_course

    response = test_client.delete("/students/delete?id=1")

    assert response.status_code == 200
    assert response.json()["name"] == "abcd"
    assert mock_course.number_of_students == 2   #(count-1)

    mock_session.query().filter().first.return_value = None  # Simulate student not found
    response = test_client.delete("/students/delete?id=1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_fetch_student_from_id(test_client, mock_student):

    mock_session.query().filter().first.return_value = mock_student
    response = test_client.get("/students/1")
    assert response.status_code == 200
    assert response == mock_student

    mock_session.query().filter().first.return_value = None  # Simulate student not found
    response = test_client.get("/students/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"