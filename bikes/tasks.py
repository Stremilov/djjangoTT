# bikes/tasks.py
from celery import shared_task
from .models import Rental
from datetime import timedelta

@shared_task
def calculate_rental_cost(rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental_duration = rental.end_time - rental.start_time
    rental_hours = rental_duration.total_seconds() / 3600
    cost = rental_hours * rental.bike.rental_rate
    rental.cost = cost
    rental.save()
