from django.shortcuts import render, get_object_or_404, redirect
import requests
import json ,re, os
from bs4 import BeautifulSoup
from oreore_project.settings import BASE_DIR


def index(request):

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
        sickcds.append("첫화면")
        sicknms.append("첫화면")

    sick = zip(sickcds,sicknms)

    return render(request, 'index.html', {
        'sick':sick,
    })

def detail_search(request, code):
    disease = find_disease_detail(code)

    context = {'disease':disease}

    return render(request, 'detail_search.html', context)


# 자체db에서 질별내용 확인
def find_disease_detail(code):
    filename = os.path.join(BASE_DIR,'data/disease_data.json')
    with open(filename, 'r') as f:
        diseases = json.load(f)

    disease_dict = {'dname_kor':'', 'kcdcode':code, 'category':'',
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

def contact(request):
    return render(request, 'contactus.html')