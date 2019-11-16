from django.shortcuts import render
from .models import *
from prescription_manage.models import *
from bs4 import BeautifulSoup as bs4
import requests, json, os, re
from django.http import JsonResponse
from oreore_project.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt

# 낱알정보 api 
def find_medicine(iscode):
    url_grn = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
    queryParams_grn = '?serviceKey=yZVErZO2RRQ0JjcdXjdNPmimESxORrD6c1Bq8Q%2BvRp1wPMKMlZ6WQOFA6wxYGMrwO9h70dTLh9Q98kNQmvOe6A%3D%3D&edi_code=' + iscode
    response2 = requests.get(url_grn+queryParams_grn).text
    bs2 = bs4(response2, 'lxml')

    # 약 이름
    medi_tag = bs2.find('item_name')
    if medi_tag:
        medi_name = medi_tag.text
    else:
        medi_name = ''

    # 약 이미지
    medi_img_tag = bs2.find('item_image')
    if medi_img_tag:
        medi_img = medi_img_tag.text
    else:
        medi_img = ''

    # 제조사
    medi_entp_tag = bs2.find('entp_name')
    if medi_entp_tag:
        medi_entp = medi_entp_tag.text
    else:
        medi_entp = ''

    # 효능
    medi_class_tag = bs2.find('class_name')
    if medi_class_tag:
        medi_class = medi_class_tag.text
    else:
        medi_class = ''


    return medi_name, medi_img, medi_entp, medi_class

# dur품목검색
def find_DUR(name,entp):
    url_dur = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/getDurPrdlstInfoList'
    queryParams = '?serviceKey=yZVErZO2RRQ0JjcdXjdNPmimESxORrD6c1Bq8Q%2BvRp1wPMKMlZ6WQOFA6wxYGMrwO9h70dTLh9Q98kNQmvOe6A%3D%3D&&entpName=' + entp + '&itemName=' + name
    response = requests.get(url_dur + queryParams).text
    result = bs4(response, 'lxml')
    print(result)

    medi_dosage_tag = result.find('ud_doc_id')
    if medi_dosage_tag:
        medi_dosage = medi_dosage_tag.text
    else:
        medi_dosage = ''
    
    medi_caution_tag = result.find('nb_doc_id')
    if medi_caution_tag:
        medi_caution = medi_caution_tag.text
    else:
        medi_caution = ''

    return medi_dosage, medi_caution

# 낱알정보 이름검색 api 
def find_medicine_name(name):
    url2 = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
    queryParams = '?serviceKey=yZVErZO2RRQ0JjcdXjdNPmimESxORrD6c1Bq8Q%2BvRp1wPMKMlZ6WQOFA6wxYGMrwO9h70dTLh9Q98kNQmvOe6A%3D%3D&item_name=' + name
    response2 = requests.get(url2+queryParams).text
    bs2 = bs4(response2, 'lxml')
    medi_tags = bs2.find_all('item')
    zip_medi_tags = zip(range(len(medi_tags)),medi_tags)
    
    result = {}

    for i,medi_item in zip_medi_tags:
        medi = {}
        medi['name'] = medi_item.find('item_name').text    
        medi['code'] = medi_item.find('edi_code').text
        medi['img'] = medi_item.find('item_image').text

        result[str(i)] = medi

    return result
    
# 약 저장
def save_medicin(iscode,pre_id):
    prescription = Prescription.objects.get(id=pre_id)

    filename = os.path.join(BASE_DIR,'data/medicine_data.json')
    with open(filename, 'r') as f:
        medicines = json.load(f)

    # 약 자체db 검색
    if iscode in medicines:
        name = medicines[iscode]['name']
        if 'img' in medicines[iscode]:
            img = medicines[iscode]['img']
        else:
            img = ''
        if 'entp' in medicines[iscode]:
            entp = medicines[iscode]['entp']
        else:
            entp = ''
        if 'class_name' in medicines[iscode]:
            class_name = medicines[iscode]['class_name']
        else:
            class_name = ''
        if 'dosage' in medicines[iscode]:
            dosage = medicines[iscode]['dosage']
        else:
            dosage = ''
        if 'caution' in medicines[iscode]:
            caution = medicines[iscode]['caution']
        else:
            caution = ''
    else:
        # 약 api검색
        name, img, entp, class_name = find_medicine(iscode)
        dosage, caution = find_DUR(name,entp)

        if not iscode in medicines:
            medicine = dict()
            medicine["name"] = name
            medicine['img'] = img
            medicine['entp'] = entp
            medicine['class_name'] = class_name
            medicine['dosage'] = dosage
            medicine['caution'] = caution

            medicines[iscode] = medicine
            
            os.remove(filename)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(medicines, f, indent=4)

    medi = Medicine()
    medi.mediName = name
    medi.insuranceCode = iscode
    medi.linkPrescription = prescription
    medi.img_url = img
    medi.entp = entp
    medi.class_name = class_name
    medi.dosage = dosage
    medi.caution = caution
    medi.save()

# index의 약검색 api
@csrf_exempt
def search_medi(request):
    code = re.compile('^\d+')
    filename = os.path.join(BASE_DIR,'data/medicine_data.json')
    with open(filename, 'r') as f:
        medicines = json.load(f)

    if 'mediname' in request.POST:
        mediname = request.POST['mediname']

    # 약 이름으로 검색                
    result = find_medicine_name(mediname)
    
    return JsonResponse(result)





