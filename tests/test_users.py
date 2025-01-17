import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

# @pytest.mark.django_db
@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    response = client.post('/api/users/register/', {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_user_login(api_client):
    User.objects.create_user(username='testuser', password='password')
    response = api_client.post('/api/token/', {'username': 'testuser', 'password': 'password'})
    assert response.status_code == 200
