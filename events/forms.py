from django import forms
from django.contrib.auth.models import User
from .models import Event, Booking

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer']
        widgets={
        'date': forms.DateInput(attrs={'type':'date'}),
        'time': forms.TimeInput(attrs={'type':'time'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tickets']

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model= Profile
#         exclude = ['user']
#         widgets = {
#         'birth_date': forms.DateInput(attrs={'type': 'date'}),
#         }
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name','password']
#         widgets={
#         'password': forms.PasswordInput(),
#         }
