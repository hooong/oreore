from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:pre_id>', views.submit_img, name='submit_img'),
    path('confirm/<int:pre_id>', views.confirm_code, name='confirm_code'),
]