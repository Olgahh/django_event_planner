from rest_framework import serializers
from django.contrib.auth.models import User
from events.models import Event, Booking

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','organizer','title', 'description','date','time',]

class UserBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['booker']

###########################################################
class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['booker']
############################################################
class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['organizer',]
##############################################################
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password']

    def create(self,validated_data):
        new_user = User(**validated_data) #unwraps the dictionary.
        new_user.set_password(validated_data.get("password"))
        new_user.save()
        return validated_data
#################################################################
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['username']

class EventBookersSerializer(serializers.ModelSerializer):
    booker = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['bookers']
        def get_booker(self, obj):
            bookings = obj.bookings.filter(booker=obj.booker)
            return UserSerializer(bookings, many=True).data
