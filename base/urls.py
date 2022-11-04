from django.urls import path
from . import views

urlpatterns =[
    path('', views.landing, name = 'landing'),
    path('user_location', views.locationApi),
    path('user_location/id=<str:pk>', views.locationApi),
    path('search_nearby', views.search_nearby, name = 'nearbypage'),
    path('nearby/id=<str:pk>', views.nearbyApi, name='nearby_result'),
]