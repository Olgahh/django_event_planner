from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, BookingForm
# , ProfileForm,UserForm
from .models import Event, Booking
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.db.models import Q

def home(request):
    if request.user.is_anonymous: #if the user is not logged go to the login page
        return redirect('login')
    return render(request, 'home.html')


def dashboard(request):
    if request.user.is_anonymous: #if the user is not logged go to the login page
        return redirect('login')
    # users_events = Event.objects.filter(organizer = request.user)
    users_events = request.user.events.all()
    today = datetime.today()
    bookers = request.user.bookers.filter(event__date__lt=today)
    context={
    "users_events" :users_events,
    "bookers":bookers
    }
    return render(request, 'dashboard.html', context)

def book_event(request, event_id):
    if request.user.is_anonymous: #if the user is not logged go to the login page
        return redirect('login')
    event = Event.objects.get(id=event_id)
    form = BookingForm()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booked_event = form.save(commit=False)
            booked_event.event=event
            booked_event.booker=request.user
            seats = event.available_seats()
            if booked_event.tickets <= seats :
                booked_event.save()
                messages.success(request,"You have successfully created a booking for this event.")
                return redirect('event-detail', event_id)
            else:
                messages.warning(request,"Not enough seats to book.")
    context ={
    "form":form,
    "event":event
    }
    return render(request,"book_event.html", context)


def event_list(request):
    if request.user.is_anonymous: #if the user is not logged go to the login page
        return redirect('login')
    today = datetime.today()
    events = Event.objects.filter(date__gte = today)
    query = request.GET.get("q")
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
            ).distinct()

    context = {
        "events" : events
    }
    return render(request,"list.html",context)



def event_detail(request,event_id):
    if request.user.is_anonymous: #if the user is not logged go to the login page
        return redirect('login')
    event = Event.objects.get(id=event_id)
    context = {
        "event" : event
    }
    return render(request,"detail.html",context)

def create_event(request):
    if request.user.is_anonymous: #if the user is not logged go to the login page
        return redirect('login')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.organizer=request.user
            new_event.save()
            messages.success(request,"You have successfully created an event.")
            return redirect('dashboard')
    context={
    "form":form
    }

    return render(request,"create.html", context)

def event_update(request,event_id):
    if request.user.is_anonymous: #if the user is not logged go to the login page
        return redirect('login')
    event = Event.objects.get(id=event_id)
    form=EventForm(instance=event)
    if request.user == event.organizer:
        if request.method == "POST":
            form=EventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request,"You have successfully edited this event.")
                return redirect('event-detail', event_id)
    context={
    "form":form,
    "event": event
    }
    return render(request,"update.html", context)


#Authentication views

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('home')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")
#
# def profile_view(request,user_id):
#     profile = Profile.objects.get(user_id=user_id)
#     context = {
#     'profile':profile
#     }
#     return render(request,'profile.html', context)
#
# def profile_update(request):
#     if request.user.is_anonymous: #if the user is not logged go to the login page
#         return redirect('login')
#     if request.method == 'POST':
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(request.POST, request.FILES,instance= request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)
#             user.save()
#             profile_form.save()
#             messages.success(request, "You have successfully updated your profile")
#             login(request, user)
#             return redirect('profile',user_id)
#         else:
#             user_form = UserForm(instance=request.user)
#             profile_form = ProfileForm(instance=request.user.profile)
#     else:
#         user_form = UserForm()
#         profile_form = ProfileForm()
#     context =  {
#         'user_form': user_form,
#         'profile_form': profile_form,
#     }
#     return render(request, 'update_profile.html',context)
