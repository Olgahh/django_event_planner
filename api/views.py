from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from events.models import Booking, Event
from .serializers import BookingSerializer, BookingCreateSerializer


class BookingList(ListAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingListSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['name', 'location']


class EventDetails(RetrieveAPIView):
	queryset = Hotel.objects.all()
	serializer_class = HotelDetailsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'hotel_id'

#1 List  of all upcoming events
class EventList(ListAPIView):
	serializer_class = EventDetailsSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		today = datetime.today()
		return Event.objects.get(datetime__gte=today)


class BookHotel(CreateAPIView):
	serializer_class = BookHotelSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user, hotel_id=self.kwargs['hotel_id'])


# class BookingView(APIView):
# 	def get(self, request, booking_id=None):
# 		if booking_id:
# 			booking = Booking.objects.get(id=booking_id)
# 			serializer = BookingSerializer(booking)
# 			return Response(serializer.data)
# 		bookings = Booking.objects.all()
# 		serializer = BookingSerializer(bookings, many=True)
# 		return Response(serializer.data)
#
# 	def post(self, request, booking_id):
# 		self.permission_classes = [IsAuthenticated]
# 		self.check_permissions(request)
# 		serializer = BookingCreateSerializer(data=request.data)
# 		if serializer.is_valid():
# 			booking = Booking.objects.get(id=booking_id)
# 			serializer.save(booking=booking, user=request.user)
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# 	def put(self, request, booking_id):
# 		self.permission_classes = [IsAuthenticated, IsBookingOwnerOrStaff]
# 		booking = Booking.objects.get(id=booking_id)
# 		self.check_object_permissions(request, booking)
# 		serializer = BookingCreateSerializer(booking, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_200_OK)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# 	def delete(self, request, booking_id):
# 		self.permission_classes = [IsAuthenticated, IsAdminUser]
# 		self.check_permissions(request)
# 		booking = Booking.objects.get(id=booking_id)
# 		booking.delete()
# 		return Response(status=status.HTTP_204_NO_CONTENT)
