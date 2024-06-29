import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from bikes.models import Bike, Rental
from django.utils import timezone

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser', password='password')
    return user

@pytest.mark.django_db
def test_bike_list(api_client, create_user):
    api_client.login(username='testuser', password='password')
    response = api_client.get('/api/bikes/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_rent_bike(api_client, create_user):
    api_client.login(username='testuser', password='password')
    bike = Bike.objects.create(name='Bike1', status='available')
    response = api_client.post(f'/api/bikes/{bike.id}/rent/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_return_bike(api_client, create_user):
    api_client.login(username='testuser', password='password')
    bike = Bike.objects.create(name='Bike1', status='available')
    Rental.objects.create(user=create_user, bike=bike, start_time=timezone.now())
    response = api_client.post(f'/api/bikes/{bike.id}/return/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_rental_history(api_client, create_user):
    api_client.login(username='testuser', password='password')
    response = api_client.get('/api/bikes/history/')
    assert response.status_code == 200
