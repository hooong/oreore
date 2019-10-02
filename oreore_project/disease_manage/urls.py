from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:pre_id>', views.add_disease, name='add_disease'),
    path('add/topre.<int:pre_id>', views.add_disease_to_prescription, name='add_disease_to_prescription')
]