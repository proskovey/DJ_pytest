import pytest
import json
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth.models import User

from students.models import Course, Student
from pprint import pprint

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory




@pytest.mark.django_db
def test_get_first_course(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get('/api/v1/courses/1/')
    assert response.status_code == 200
    assert response.data['name'] == courses[0].name

@pytest.mark.django_db
def test_get_list_courses(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name

@pytest.mark.django_db
def test_filter_id(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?id={courses[5].pk}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[5].pk


@pytest.mark.django_db
def test_filter_name(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?name={courses[3].name}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[3].name

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'id': 1, 'name': 'course_1'}, format='json')
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_update_course(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.patch(f'/api/v1/courses/{courses[0].pk}/', data={'id': 1, 'name': 'course_update'}, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'course_update'

@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    courses = courses_factory(_quantity=10)
    count = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{courses[0].pk}/')
    assert response.status_code == 204
    assert Course.objects.count() == count - 1