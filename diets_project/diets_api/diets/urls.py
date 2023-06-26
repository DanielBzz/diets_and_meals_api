from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.diets_view),
    path('/<name>', views.diet_view)
]