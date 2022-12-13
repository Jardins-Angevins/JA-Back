import numpy as np
import requests
from PIL import Image
import base64
import IA.resize_algorithm as re
import app

def test_query():
    url = 'http://localhost:5001/query'
    image_pil = Image.open("/home/etud/PycharmProjects/JA-Angers/datas/tela_botanica_images_min/IMG_100897_000046845CRS.jpg")
    image = np.array(image_pil)
    image = list(re.img_crop(image,(app.IMAGE_SIZE,app.IMAGE_SIZE)))[0]
    image = base64.b64encode(image).decode("utf-8")
    response = requests.post(url, json={'image64': image})
test_query()