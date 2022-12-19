import unittest
import requests
import json
import numpy
import base64

from PIL import Image

# ---
# Allowing import of project root folder
import sys
sys.path.append('.')
# ---

from ia import resize_algorithm as re

BASE_URL = 'http://localhost:8088/query'

class TestQueryRoute(unittest.TestCase):

	def setUp(self):
		# Open up file and get pixel to an numpy matrix
		image = numpy.array( Image.open("./datas/tela_botanica_images_min/IMG_100897_000046845CRS.jpg") )
		# Crop up only the interresting pixels
		correctImage = list( re.img_crop( image , (256,256) ) )[0]
		incorrectImage = list( re.img_crop( image , (100,200) ) )[0]
		# Encode into base64 format
		correctImage = base64.b64encode(correctImage).decode("utf-8")
		incorrectImage = base64.b64encode(incorrectImage).decode("utf-8")
		self.incorrectImage = incorrectImage 
		self.correctImage = correctImage

	def test_fetch(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":3,"long":3} )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 201 )
		self.assertIsInstance( data['prediction'] ,        int )

	def test_missing_mandatory_arg_lat(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"long":3} )
		self.assertEqual( response.status_code , 400 )
		
	def test_missing_mandatory_arg_long(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":3} )
		self.assertEqual( response.status_code , 400 )
	
	def test_wrong_type_on_arg_lat(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":"dzez","long":3} )
		self.assertEqual( response.status_code , 400 )
		
	def test_wrong_type_on_arg_long(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"long":"dep","lat":3} )
		self.assertEqual( response.status_code , 400 )

	def test_missing_body(self):
		response = requests.post( BASE_URL , json={}, params={"lat":3,"long":3} )
		self.assertEqual( response.status_code , 400 )

	def test_wrong_type_on_body(self):
		response = requests.post( BASE_URL , json={'image64' : '1#3z_|'},params={"lat":3,"long":3} )
		self.assertEqual( response.status_code , 400 )

	def test_invalid_image_in_body(self):
		response = requests.post( BASE_URL , json={'image64' : self.incorrectImage},params={"lat":3,"long":3} )
		self.assertEqual( response.status_code , 400 )

	def test_invalid_image_in_body_sneakier(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage.replace('4','ù').replace('o','`')},params={"lat":3,"long":3} )
		self.assertEqual( response.status_code , 400 )

	