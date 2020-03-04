from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
CreateAPIView, ListAPIView,
RetrieveAPIView,RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from events.models import Booking, Event
from .serializers import (
RegisterSerializer, EventListSerializer,
UserBookingSerializer, CreateBookingSerializer,
CreateSerializer,EventBookersSerializer)
from datetime import datetime
from .permissions import  IsOrganizer

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

#1 List  of all upcoming events
class UpcomingEventList(ListAPIView):
    serializer_class = EventListSerializer
    filter_backends = [SearchFilter,]
    search_fields = ['title', 'description','organizer']
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
         today = datetime.today()
         return Event.objects.filter(datetime__gte=today)

#2 List of events for a specific organizer
class EventforSpecificOrganizerList(ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        organizer = self.kwargs['organizer_username']
        return Event.objects.filter(organizer__username = organizer )

#3 List of events I have booked for, as a logged in user
class UserBookingList(ListAPIView):
    serializer_class = UserBookingSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return  Booking.objects.filter(booker=self.request.user)

#9 As a user I can book for an event.
class BookCreateView(CreateAPIView) :
    serializer_class = CreateBookingSerializer
    permission_classes = [IsAuthenticated,]
    def perform_create (self, serializer) :
        serializer.save(booker=self.request.user)

# As an event organizer I can create/update an event.
class EventCreateView(CreateAPIView) :
    serializer_class = CreateSerializer
    permission_classes = [IsAuthenticated,IsOrganizer]
    def perform_create(self, serializer) :
        serializer.save(organizer=self.request.user)
class EventUpdateView(RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated,IsOrganizer]
    serializer_class = CreateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'

# As an event organizer I can retrieve a list of people who have booked for an event.
class BookerDetails(RetrieveAPIView):
        serializer_class = EventBookersSerializer
        lookup_field = 'id'
        lookup_url_kwarg = 'event_id'
        permission_classes = [IsAuthenticated,IsOrganizer]
        def get_queryset(self):
            return  Event.objects.filter(organizer=self.request.user)
