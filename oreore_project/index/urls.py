from django.urls import path
from . import views


urlpatterns = [
    path('detail_search/<str:code>/', views.detail_search, name='detail_search'),

]