from django.shortcuts import render,redirect
from urllib.request import urlopen
from django.utils.http import urlencode
from django.utils.six.moves.urllib.parse import quote_plus
import requests, json, os, io
import xml.etree.ElementTree as ET
from oreore_project.settings import BASE_DIR

# read_prescription
def read_pres():
    pic = os.path.join(BASE_DIR,'pres_images/4.jpeg')

    recipt = detect_text(pic)

    return


# 로컬이미지
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    # OCR로 읽은 전체 문자열
    pres_text = texts[0].description
    print(pres_text)

    return pres_text


# 원격이미지
def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient() 
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

# 낱알정보 api 
def find_medicine(request):
    edicode = '642102570'
    url = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
    queryParams = '?serviceKey=yZVErZO2RRQ0JjcdXjdNPmimESxORrD6c1Bq8Q%2BvRp1wPMKMlZ6WQOFA6wxYGMrwO9h70dTLh9Q98kNQmvOe6A%3D%3D&edi_code=' + edicode

    # result = urllib2.urlopen( url + queryParams)
    request = requests.get(url + queryParams)
    # response = result.read()
    # print(response)
        
    # request = urllib.request.Request(url+queryParams)
    # response = urllib.request.urlopen(request)
    # print (response.read().decode('utf-8'))
    r = request.text
    print(r)
    root = ET.fromstring(r)

    read_pres()
    

    # print(request.text)
    # responses = ET.fromstring(request.text)
    # print(responses.text)
    # for response in responses:
    #     print(response.tag, response.attrib)

    return redirect('index')