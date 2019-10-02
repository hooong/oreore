from django.shortcuts import render
from prescription_manage.models import *


def index(request):


    return render(request,'index.html')