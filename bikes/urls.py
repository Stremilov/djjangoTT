from django.urls import path
from .views import BikeListView, RentBikeView, ReturnBikeView, RentalHistoryView

urlpatterns = [
    path('bikes/', BikeListView.as_view(), name='bike-list'),
    path('bikes/rent/<int:bike_id>/', RentBikeView.as_view(), name='rent-bike'),
    path('bikes/return/<int:rental_id>/', ReturnBikeView.as_view(), name='return-bike'),
    path('rentals/', RentalHistoryView.as_view(), name='rental-history'),
]
