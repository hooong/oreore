from django.urls import path
from . import views

urlpatterns = [
    path('noti/', views.predict_month, name='noti')
]