"""event_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

from api.views import RegisterView, UpcomingEventList, EventforSpecificOrganizerList, UserBookingList,BookCreateView, EventCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', include('events.urls')),
    # APIs
    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/upcomingevent/list/', UpcomingEventList.as_view(), name='api-upcoming-list'),
    path('api/<str:organizer_username>/list', EventforSpecificOrganizerList.as_view(), name='api-organizer-list'),
    path('api/bookings/list/',  UserBookingList.as_view(), name='api-bookings-list'),
    path('api/create/', BookCreateView.as_view(), name='api-event-create'),
    path('api/create/update', EventCreateView.as_view(), name='api-event-create-update'),


]


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
