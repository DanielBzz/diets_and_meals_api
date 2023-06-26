from django.urls import path
from . import views

urlpatterns = [
    path('', views.meals_url_method),
    path('/<id_or_name>', views.meal_url_method)
]