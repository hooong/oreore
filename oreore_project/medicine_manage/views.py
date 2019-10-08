from django.shortcuts import render
from .models import *
from prescription_manage.models import *
from bs4 import BeautifulSoup as bs4
import requests

# 낱알정보 api 
def find_medicine(iscode):
    url2 = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
    queryParams = '?serviceKey=yZVErZO2RRQ0JjcdXjdNPmimESxORrD6c1Bq8Q%2BvRp1wPMKMlZ6WQOFA6wxYGMrwO9h70dTLh9Q98kNQmvOe6A%3D%3D&edi_code=' + iscode
    response2 = requests.get(url2+queryParams).text
    bs2 = bs4(response2, 'lxml')
    medi_tag = bs2.find('item_name')
    if medi_tag:
        medi_name = medi_tag.text
    else:
        medi_name = ''

    medi_img_tag = bs2.find('item_image')
    if medi_img_tag:
        medi_img = medi_img_tag.text
    else:
        medi_img = ''

    return medi_name, medi_img
    
# 약 저장
def save_medicin(iscode,pre_id):
    prescription = Prescription.objects.get(id=pre_id)
    name, img = find_medicine(iscode)

    medi = Medicine()
    medi.mediName = name
    medi.insuranceCode = iscode
    medi.linkPrescription = prescription
    medi.img_url = img
    medi.save()


