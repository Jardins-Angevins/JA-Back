import numpy as np
import requests
import base64

IMAGE_SIZE = (256,256)
def test_map():
    url = 'http://localhost:8088/map'
    response = requests.get(url,params={'long':3,'lat':3,'dlat':3,'dlong':3})

    print(response.text,response.status_code)

test_map()