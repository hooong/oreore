from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:pre_id>', views.add_disease, name='add_disease'),
    path('topre/<int:pre_id>/<str:code>/<str:name>', views.add_disease_to_prescription, name='add_disease_to_prescription')
]