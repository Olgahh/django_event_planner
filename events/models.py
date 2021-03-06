from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, default = 1, related_name='events')
    title = models.CharField(max_length=120)
    date= models.DateField(null=True)
    time=models.TimeField(null=True)
    description = models.TextField()
    location = models.CharField(max_length=120)
    seats = models.IntegerField()
    image = models.ImageField(blank=True,null=True)

    def __str__(self):
        return f"Event title: {self.title}"

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})

    def tickets_booked(self):
        return sum(self.bookings.all().values_list('tickets', flat=True)) # will sum the number of booked ticket

    def available_seats(self):
        return self.seats - self.tickets_booked()



class Booking(models.Model):
    booker = models.ForeignKey(User, on_delete=models.CASCADE, default = 1,related_name="bookers" )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default = 1,related_name="bookings")
    tickets = models.PositiveIntegerField()

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE,  default = 1, related_name='profile')
#     img = models.ImageField(blank=True,null=True)
#     about_me = models.TextField(max_length=800, blank=True)
#     dob = models.DateField(null=True, blank=True)
#     def get_name(self):
#             name = '%s %s' % (self.first_name, self.last_name)
#             return name.strip()
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
