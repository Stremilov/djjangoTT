from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from .models import Bike, Rental
from .serializers import BikeSerializer, RentalSerializer
from .tasks import calculate_rental_cost


class BikeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bikes = Bike.objects.filter(is_available=True)
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data)

class RentBikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, bike_id):
        user = request.user
        if Rental.objects.filter(user=user, end_time__isnull=True).exists():
            return Response({'detail': 'User already has an active rental.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bike = Bike.objects.get(id=bike_id, is_available=True)
        except Bike.DoesNotExist:
            return Response({'detail': 'Bike not available.'}, status=status.HTTP_404_NOT_FOUND)

        rental = Rental.objects.create(user=user, bike=bike)
        bike.is_available = False
        bike.save()
        return Response(RentalSerializer(rental).data, status=status.HTTP_201_CREATED)

class ReturnBikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, bike_id):
        try:
            bike = Bike.objects.get(id=bike_id, status='rented', rental__user=request.user)
            rental = Rental.objects.get(bike=bike, user=request.user, end_time__isnull=True)
            rental.end_time = timezone.now()
            rental.save()
            bike.status = 'available'
            bike.save()
            calculate_rental_cost.delay(rental.id)
            return Response({'message': 'Bike returned successfully'}, status=status.HTTP_200_OK)
        except Bike.DoesNotExist:
            return Response({'error': 'Bike not found or not rented by user'}, status=status.HTTP_404_NOT_FOUND)

class RentalHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rentals = Rental.objects.filter(user=request.user)
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data)
