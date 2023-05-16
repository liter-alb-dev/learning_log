"""Defines URL patterns for user_manager"""

from django.urls import path, include

from . import views

app_name = 'user_manager'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
]