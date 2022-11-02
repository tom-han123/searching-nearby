from django.urls import path
from . import views

urlpatterns =[
    path('', views.landing, name = 'landing'),
    path('user/location', views.locationApi),
    path('user/<str:pk>/location', views.locationApi),
    path('user/<str:pk>/location/<int:lpk>', views.locationApi),
    path('nearby/<str:loc>', views.nearbyApi),
]