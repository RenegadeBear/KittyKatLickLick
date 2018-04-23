from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('travels', views.travels),
    path('login', views.login),
    path('trip/<id>', views.trip),
    path('join/<id>', views.join),
    path('add', views.add),
    path('add_trip', views.add_trip),
    path('logout', views.logout)
]