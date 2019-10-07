from django.shortcuts import render, get_object_or_404, redirect
import requests
import json ,re
from bs4 import BeautifulSoup
from .models import *
from prescription_manage.models import *

def add_disease(request, pre_id):
    sicknm = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    pattern = re.compile('[가-힣]')
    m = pattern.match(sicknm)
    sickcds = []
    sicknms = []

    if sicknm: # q가 있으면
        if m:
            url = 'http://apis.data.go.kr/B551182/diseaseInfoService/getDissNameCodeList'
            servicekey = '?serviceKey=mF0R4JkA1iQum90bD2LlrTOLwW7fTLc9O30vp71HxeJ%2FuEUZvx8c1vFraeFHvj5DHOWx%2FtGH7p2VaqoCtKQDpg%3D%3D'
            queryParams = '&diseaseType=SICK_NM&searchText=' + sicknm
            response = requests.get(url+servicekey+queryParams).text
            bs = BeautifulSoup(response, 'lxml')
            # print(jsonString)
        else:
            url = 'http://apis.data.go.kr/B551182/diseaseInfoService/getDissNameCodeList'
            servicekey = '?serviceKey=mF0R4JkA1iQum90bD2LlrTOLwW7fTLc9O30vp71HxeJ%2FuEUZvx8c1vFraeFHvj5DHOWx%2FtGH7p2VaqoCtKQDpg%3D%3D'
            queryParams = '&diseaseType=SICK_CD&searchText=' + sicknm
            response = requests.get(url+servicekey+queryParams).text
            bs = BeautifulSoup(response, 'lxml')
            # print(jsonString)
        sicknm = bs.find_all('sicknm')
        sickcd = bs.find_all('sickcd')


        if sicknm == []:
            sickcds.append("검색 내용 없음")
            sicknms.append("검색 내용 없음")
        else:
            for el in sicknm:
                # 'J' 검색시 // 이게 str패턴에 맞지않아 문제발생 따라서 미리 //를 제거해주었음.
                el = re.sub('//', '', el.text)
                sicknms.append(el)
            for el in sickcd:
                sickcds.append(el.text)   
            # print(els)
            
            
    else:
        sickcds.append("검색 내용 없음")
        sicknms.append("검색 내용 없음")

    sick = zip(sickcds,sicknms)
    return render(request, 'add_disease.html', {
        'sick':sick,
        'res2':res2,
        'pre_id':pre_id
    })

def add_disease_to_prescription(request, pre_id, code, name):
    disease = Disease()
    disease.diesName = name
    disease.kcdCode = code
    disease.linkPrescription = Prescription.objects.get(id=pre_id)
    disease.save()

    return redirect('/disease/add/' + str(pre_id) + '?q=')
