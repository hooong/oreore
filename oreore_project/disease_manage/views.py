from django.shortcuts import render, get_object_or_404, redirect
import requests
import json ,re
from bs4 import BeautifulSoup

def add_disease(request, pre_id):
    sicknm = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    pattern = re.compile('[가-힣]')
    m = pattern.match(sicknm)

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
        sickcds = []
        sicknms = []

        if sicknm == []:
            sickcds.append("검색 내용 없음")
            sicknms.append("검색 내용 없음")
        else:
            
            for el in sicknm:
                sicknms.append(el.text)
            for el in sickcd:
                sickcds.append(el.text)   
            # print(els)
            
            
    else:
        sickcd ="검색 내용 없음"
        sicknm = "검색 내용 없음"

    edicode = "642102570"
    url2 = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
    queryParams = '?serviceKey=yZVErZO2RRQ0JjcdXjdNPmimESxORrD6c1Bq8Q%2BvRp1wPMKMlZ6WQOFA6wxYGMrwO9h70dTLh9Q98kNQmvOe6A%3D%3D&edi_code=' + edicode
    response2 = requests.get(url2+queryParams).text
    bs2 = BeautifulSoup(response2, 'lxml')
    # print(jsonString)
    result2 = bs2.find('item_name')
    print(result2.text)
    res2 = result2.text

    img = bs2.find('item_image')
    img=img.text
    sick = zip(sickcds,sicknms)
    return render(request, 'add_disease.html', {
        'sick':sick,
        'img':img,
        'res2':res2,
        'pre_id':pre_id
    })

def add_disease_to_prescription(request,pre_id):

    return redirect('/disease/add/' + str(pre_id) + '?q=K')
