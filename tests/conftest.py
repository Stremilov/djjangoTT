import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from bikes.models import Bike

import pytest
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import call_command

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    call_command('migrate')

@pytest.fixture(scope='module')
def django_db_blocker():
    pass

