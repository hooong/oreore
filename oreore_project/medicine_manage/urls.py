from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_medi, name='search_medi')
]