from django.urls import path
from . import views

urlpatterns =[
    path('', views.landing, name = 'landing'),
    path('user_location', views.locationApi),
    path('user_location/id=<str:pk>', views.locationApi),
    path('nearby/id=<str:pk>&range=<str:rng>&gender=<str:gen>&age=<str:age>', views.nearbyApi),
]