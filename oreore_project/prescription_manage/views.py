from django.shortcuts import render, redirect
from .models import *
from disease_manage.models import *
from medicine_manage.models import *
import json, os
from oreore_project.settings import BASE_DIR

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
    diszip = zip(disease,range(30))
    context = {
        'medi':medi,
        'pre':prescription,
        'dis':disease,
        'diszip':diszip,
        
        
    }

    return render(request, 'detail_prescription.html', context)

def mod_medicine_view(request, code, pre_id):
    context = {'code':code, 'pre_id':pre_id}

    return render(request, "mod_medicine.html", context)

def mod_medicine(request):
    pre_id = request.POST['pre_id']
    medi_name = request.POST['medi_name']
    code = request.POST['insurcode']

    # json data 수정 및 추가
    medicine = dict()
    medicine["name"] = medi_name

    filename = os.path.join(BASE_DIR,'data/medicine_data.json')
    with open(filename, 'r') as f:
        data = json.load(f)
        data[code] = medicine

    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    # db내용 수정
    pre = Prescription.objects.get(id=pre_id)
    medicine = Medicine.objects.get(linkPrescription=pre, insuranceCode=code)
    medicine.mediName = medi_name
    medicine.save()
        
    return redirect('/prescription/detail/'+str(pre_id))