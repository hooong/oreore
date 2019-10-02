from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.all_prescription, name="all_prescription"),
    path('add/', views.add_prescription, name='add_prescription'),
]