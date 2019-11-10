from django.shortcuts import render, redirect
from .models import *
from disease_manage.models import *
from medicine_manage.models import *
import json, os
from oreore_project.settings import BASE_DIR

def all_prescription(request):
    # 처방전 (로그인 한 사람만 들어올수있는페이지)
    if request.user.is_authenticated:
        prescriptions = Prescription.objects.filter(ownUser=request.user).order_by('-id')
        
        disease = []
        for pre in prescriptions:
            diseases = Disease.objects.filter(linkPrescription=pre)
            for dis in diseases:
                if not dis.kcdCode == '검색 내용 없음':
                    disease.append(dis.kcdCode)

        disease = list(set(disease))
        
        context = {
            'prescriptions': prescriptions,
            'disease': disease,
        }
    else:
        context = {}
    
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
    diseases = Disease.objects.filter(linkPrescription=prescription)
    medi = Medicine.objects.filter(linkPrescription=prescription)
    if not medi:
        medi = ['empty'] # 약품정보가 없을때

    disease_list = []

    for disease in diseases:
        disease_dict = find_disease_detail(disease)
        disease_list.append(disease_dict)
    if disease_list == [] :
        disease_list = ['empty'] # 리스트에 없을때를 구분하기위해
        
    diszip = zip(disease_list,range(30))
    context = {
        
        'medi':medi,
        'pre':prescription,
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

# 자체db에서 질별내용 확인
def find_disease_detail(disease):
    filename = os.path.join(BASE_DIR,'data/disease_data.json')
    with open(filename, 'r') as f:
        diseases = json.load(f)

    code = disease.kcdCode
    disease_dict = {'dname_kor':disease.diesName, 'kcdcode':disease.kcdCode, 'category':'',
                    'dname_eng':'', 'definition':'', 'cause':'', 'symptom':'',
                    'treatment':'', 'etc':'', 'lifestyle':''}
    
    if code in diseases:
        disease_dict = paste_detail(diseases,disease_dict,code)
    elif (code[:-1] + '-') in diseases:
        disease_dict = paste_detail(diseases,disease_dict,code[:-1]+'-')
    elif (code+'-') in diseases:
        disease_dict = paste_detail(diseases,disease_dict,code+'-')
    
    return disease_dict

# 자체db에서 내용 복사
def paste_detail(disease,disease_dict,code):
    disease_dict['dname_kor'] = disease[code]['Dname_kor']
    disease_dict['category'] = disease[code]['Category']
    disease_dict['dname_eng'] = disease[code]['Dname_eng']
    disease_dict['definition'] = disease[code]['Definition']
    disease_dict['cause'] = disease[code]['Cause']
    disease_dict['symptom'] = disease[code]['Symptom']
    disease_dict['treatment'] = disease[code]['Treatment']
    disease_dict['etc'] = disease[code]['etc']

    return disease_dict
