from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.all_prescription, name="all_prescription"),
    path('add/', views.add_prescription, name='add_prescription'),
    path('detail/<int:pre_id>', views.detail_prescription, name='detail_prescription'),
    path('mod/', views.mod_medicine, name="mod_medicine")
]