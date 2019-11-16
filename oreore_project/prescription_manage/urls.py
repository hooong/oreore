from django.urls import path
from . import views


urlpatterns = [
    path('all/', views.all_prescription, name="all_prescription"),
    path('add/', views.add_prescription, name='add_prescription'),
    path('delete/<int:pre_id>', views.del_prescription, name="del_prescription"),
    path('detail/<int:pre_id>', views.detail_prescription, name='detail_prescription'),
    path('mod/<str:code>/<int:pre_id>/', views.mod_medicine_view, name="mod_medicine_view"),
    path('mod_save/', views.mod_medicine, name="mod_medicine"),
]