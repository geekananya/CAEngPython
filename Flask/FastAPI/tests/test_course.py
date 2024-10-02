from unittest.mock import Mock
import pytest
from Flask.FastAPI import models
from Flask.FastAPI.tests.test_main import mock_session


@pytest.mark.parametrize("course_data, expected_status, expected_detail", [
    ({"name": "Course 1", "number_of_students": 0}, 200, None),
    ({"name": "Course 2", "number_of_students": 0}, 200, None),
])
def test_create_course(test_client, course_data, expected_status, expected_detail):
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()

    response = test_client.post("/courses/create", json=course_data)

    assert response.status_code == expected_status
    if expected_detail:
        assert response.json()["detail"] == expected_detail
    else:
        assert response.json()["name"] == course_data["name"]


def test_update_course(test_client):
    course_id = 1
    new_name = "new name"
    mock_course = models.Course(course_id=1, name="old name", number_of_students=0)
    mock_session.query().filter().first.return_value = mock_course

    response = test_client.put(f"/courses/update?id={course_id}&new_name={new_name}")

    assert response.status_code == 200
    assert response.json()["name"] == new_name

def test_delete_course(test_client):
    course_id = 1
    mock_course = models.Course(course_id=1, name="Course 1", number_of_students=0)
    mock_session.query().filter().first.return_value = mock_course

    response = test_client.delete(f"/courses/delete?id={course_id}")

    assert response.status_code == 200
    assert response.json()["name"] == mock_course.name

def test_fetch_courses(test_client):
    mock_session.query().limit().all.return_value = [
        models.Course(name="Course 1", number_of_students=0),
        models.Course(name="Course 2", number_of_students=0)
    ]
    response = test_client.get("/courses?limit=100")

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_fetch_course_from_id(test_client):
    course_id = 1
    mock_course = models.Course(course_id=1, name="Course 1", number_of_students=0)
    mock_session.query().filter().first.return_value = mock_course

    response = test_client.get(f"/courses/{course_id}")

    assert response.status_code == 200
    assert response.json()["name"] == mock_course.name