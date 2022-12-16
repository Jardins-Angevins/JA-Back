import numpy as np
import requests
from PIL import Image
import base64
from ia import resize_algorithm as re

IMAGE_SIZE = (256,256)

def test_query():
    url = 'http://localhost:8088/query'
    image_pil = Image.open("./datas/tela_botanica_images_min/IMG_100897_000046845CRS.jpg")
    image = np.array(image_pil)
    image = list(re.img_crop(image,IMAGE_SIZE))[0]
    image = base64.b64encode(image).decode("utf-8")
    response = requests.post(url, json={'image64': image},params={"lat":3,"long":3})
    print(response.text,response.status_code)

def test_statistics():
    url = 'http://localhost:8088/statistics'
    response = requests.get(url)
    print(response.text,response.status_code)

def test_species():
    url = 'http://localhost:8088/species'
    response = requests.get(url,params={'nominalNumber':99501})
    print(response.text,response.status_code)


def test_map():
    url = 'http://localhost:8088/map'
    response = requests.get(url,params={'long':3,'lat':3,'dlat':3,'dlong':3})

    print(response.text,response.status_code)

test_statistics()
test_species()
test_query()
test_map()