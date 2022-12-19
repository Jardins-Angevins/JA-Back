import unittest
import requests
import json

BASE_URL = 'http://localhost:8088/species'

class TestSpeciesRoute(unittest.TestCase):

	def test_fetch(self):
		response = requests.get( BASE_URL ,params={ 'nominalNumber' : 992501 } )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 200 )
		self.assertIsInstance( data['name'] ,              str)
		self.assertIsInstance( data['scientificName'] ,    str)
		self.assertIsInstance( data['refImage'] ,          str)
		self.assertIsInstance( data['stats']['water'] ,    int)
		self.assertIsInstance( data['stats']['light'] ,    int)
		self.assertIsInstance( data['stats']['toxicity'] , int)

	def test_missing_mandatory_arg(self):
		response = requests.get( BASE_URL )
		self.assertEqual( response.status_code , 400 )

	def test_wrong_type_on_arg(self):
		response = requests.get( BASE_URL , params={ 'nominalNumber' : 'imNotAnInteger' })
		self.assertEqual( response.status_code , 400 )

	def test_not_existing_data(self):
		response = requests.get( BASE_URL , params={ 'nominalNumber' : 6664269 })
		self.assertEqual( response.status_code , 404 )
