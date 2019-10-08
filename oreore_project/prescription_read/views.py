from django.shortcuts import render,redirect
from urllib.request import urlopen
from django.utils.http import urlencode
from django.utils.six.moves.urllib.parse import quote_plus
from google.cloud import vision
import requests, json, os, io, re
from oreore_project.settings import BASE_DIR
from .forms import *
from .models import *
from prescription_manage.models import *
from medicine_manage.views import *

# read_prescription
def read_pres(user):
    # 읽을 사진 모델 찾기
    pre_img_model = Prescription_img.objects.get(user=user)

    # 저장된 사진 path찾기
    path = pre_img_model.pre_img.url
    img_path = os.path.join(BASE_DIR,path[1:])      # os.path.join() 쓸때 뒤에꺼에 '/'가 들어가면 안됨.

    # ocr api돌리기
    pre_text = detect_text(img_path)

    # 읽은 파일 및 모델 삭제
    os.remove(img_path)
    pre_img_model.delete()

    iscode = collect_code(pre_text)

    return iscode


# 로컬이미지
def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    # OCR로 읽은 전체 문자열
    pres_text = texts[0].description

    return pres_text

# 처방전 이미지 업로드
def submit_img(request, pre_id):
    if request.method == 'POST':
        pre_img_form = Prescription_imgForm(request.POST, request.FILES)
        if pre_img_form.is_valid():
            pre_img = pre_img_form.save(commit=False)
            pre_img.user = request.user
            pre_img.save()

        return redirect('/prescription_read/confirm/' + str(pre_id))
    else:
        pre_img_form = Prescription_imgForm()
        
        context = {
            'pre_img_form' : pre_img_form,
            'pre_id': pre_id
        }
        return render(request, 'submit_img.html', context)


# 정규식으로 보험코드 따내기
def collect_code(text):
    m = re.compile(r'\d{9}')
    collect = m.findall(text)

    return collect


# OCR 후 입력값 확인받기
def confirm_code(request,pre_id):
    if request.method == 'POST':
        prescription = Prescription(id=pre_id)

        # 낱알 api로 약 정보 불러와야함.
        iscode_str = request.POST['iscode[]']

        iscode_list = iscode_str.split(',')

        for iscode in iscode_list:
            find_medicine(iscode)
        
        for iscode in iscode_list:
            save_medicin(iscode,pre_id)

        return redirect('all_prescription')
    else:
        # iscode 읽어오기
        iscode_list = read_pres(request.user)

        return render(request, 'confirm_code.html', {'iscode':iscode_list, 'pre_id':pre_id})
