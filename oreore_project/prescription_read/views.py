from django.shortcuts import render,redirect
from urllib.request import urlopen
from django.utils.http import urlencode
from django.utils.six.moves.urllib.parse import quote_plus
from google.cloud import vision
import requests, json, os, io, re
from oreore_project.settings import BASE_DIR, ROOT_DIR
from .forms import *
from .models import *

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
    print(iscode)

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


# 원격이미지
def detect_text_uri(uri):
    client = vision.ImageAnnotatorClient() 
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # OCR로 읽은 전체 문자열
    pres_text = texts[0].description
    print(pres_text)

    return pres_text

# 낱알정보 api 
def find_medicine(request):
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

    return redirect('index')

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

# OCR 후 입력값 확인받기
def confirm_code(request,pre_id):
    if request.method == 'POST':
        return redirect('index')
    else:
        iscode = read_pres(request.user)
        return render(request, 'confirm_code.html', {'iscode':iscode, 'pre_id':pre_id})

# 정규식으로 보험코드 따내기
def collect_code(text):
    m = re.compile(r'\d{9}')
    collect = m.findall(text)

    return collect