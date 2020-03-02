from rest_framework import serializers
from django.contrib.auth.models import User
from event.models import Event, Booking

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['__all__']

    def create(self, validated_data):
        booker = Booking(booker=validated_data['booker'],event = validated_data['event'],tickets = validated_data['tickets'] )
        booker.save()
        return validated_data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['__all__']

class EventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['__all__']



#######################################################################################################################################
#1 List  of all upcoming events
#2 List of events for a specific organizer
#3 List of events I have booked for, as a logged in user
#4 List of organizers I am following, as a logged in user
#5 As an event organizer/user I can login
#6 As an event organizer/user I can signup.
#7 As an event organizer I can create/update an event.
#8 As an event organizer I can retrieve a list of people who have booked for an event.
#9 As a user I can book for an event.
#10 As a user I can follow/unfollow an organizer.
