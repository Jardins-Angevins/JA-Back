import numpy as np
import requests
from PIL import Image
import base64
import IA_.resize_algorithm as re

def test_query():
    url = 'http://localhost:8088/query'
    image_pil = Image.open("./datas/tela_botanica_images_min/IMG_100897_000046845CRS.jpg")
    image = np.array(image_pil)
    image = list(re.img_crop(image,(256,256)))[0]
    image = base64.b64encode(image).decode("utf-8")
    response = requests.post(url, json={'image64': image})
    print(response.text)
test_query()