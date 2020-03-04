from django.urls import path
from .views import Login, Logout, Signup, home, event_list, event_detail, create_event,event_update, book_event
from events import views

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('events/list/', event_list, name='event-list'),
    path('events/details/<int:event_id>', event_detail, name='event-detail'),
    path('events/create', create_event, name='create-event'),
    path('events/update/<int:event_id>', event_update, name='event-update'),

    path('events/details/<int:event_id>/book', book_event, name='book-event'),
]
