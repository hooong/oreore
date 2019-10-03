from django.shortcuts import render, redirect
from .models import *

def all_prescription(request):
    # 처방전 (로그인 한 사람만 들어올수있는페이지)
    prescriptions = Prescription.objects.filter(ownUser=request.user)
    
    context = {
        'prescriptions': prescriptions,
    }
    
    return render(request, 'all_prescription.html', context)

def add_prescription(request):
    if request.method == 'POST':
        add_pre = Prescription()
        add_pre.prescriptionName = request.POST['name']
        add_pre.ownUser = request.user
        add_pre.save()
        return redirect('/disease/add/' + str(add_pre.id) + '?q=')
    else:
        return render(request, 'add_prescription.html')
