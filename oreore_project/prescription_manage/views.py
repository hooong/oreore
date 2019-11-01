from django.shortcuts import render, redirect
from .models import *
from disease_manage.models import *
from medicine_manage.models import *

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

def detail_prescription(request, pre_id):
    prescription = Prescription.objects.get(id=pre_id)
    disease = Disease.objects.filter(linkPrescription=prescription)
    medi = Medicine.objects.filter(linkPrescription=prescription)

    context = {
        'medi':medi,
        'pre':prescription,
        'dis':disease,
    }

    return render(request, 'detail_prescription.html', context)

def mod_medicine(request):
    if request.method == 'POST':
        return 0
    else:
        return render(request, "mod_medicine.html")