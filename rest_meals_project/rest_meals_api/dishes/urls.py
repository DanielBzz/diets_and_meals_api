from django.urls import path
from . import views

urlpatterns = [
    path('', views.dishes_url_method),
    path('/<id_or_name>', views.dish_url_method)
]
