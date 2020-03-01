from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    title = models.CharField(max_length=120)
    datetime = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=120)
    seats = models.PositiveIntegerField()
    image = models.ImageField(blank=True,null=True)

    def __str__(self):
        return f"Event title: {self.title}"

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})

    def available_seats(self):
        # if (Event.objects.values_list('seats', flat=True)) <= (Booking.objects.values_list('tickets', flat=True)):
        #     return 0
        # else:
        tickets_booked =sum(Booking.objects.values_list('tickets', flat=True)) # will sum the number of booked tickets
        return self.seats - tickets_booked

    # def is_full(self):
    #     if self.available_seats == 0:
    #         return True
    #     else:
    #         return False

class Booking(models.Model):
    booker = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default = 1)
    tickets = models.PositiveIntegerField()
