import unittest
import requests
import json

BASE_URL = 'http://localhost:8088/species/list'

class TestSpeciesListRoute(unittest.TestCase):

	def test_fetch(self):
		response = requests.get( BASE_URL ,params={ 'page' : 0 } )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 200 )
		self.assertIsInstance( data['species'] ,                   list)
		self.assertIsInstance( data['species'][0]['image'] ,           str)
		self.assertIsInstance( data['species'][0]['name'] ,            str)
		self.assertIsInstance( data['species'][0]['nominalNumber'] ,   int)

	def test_fetch_bis(self):
		response = requests.get( BASE_URL ,params={ 'page' : 0 } )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 200 )
		self.assertIsInstance( data['species'] ,                   list)
		self.assertIsInstance( data['species'][0]['image'] ,           str)
		self.assertIsInstance( data['species'][0]['name'] ,            str)
		self.assertIsInstance( data['species'][0]['nominalNumber'] ,   int)

	def test_wrong_type_on_arg(self):
		response = requests.get( BASE_URL , params={ 'page' : 'jile' } )
		self.assertEqual( response.status_code , 400 )

	def test_no_more_page_left(self):
		p = 1
		r = 200
		while r == 200:
			response = requests.get( BASE_URL , params={ 'page' : p } )
			r = response.status_code
			# Set a max loop limit to avoid infinite loop in certain cases, safe cap might need some ajustment
			if p > 2**12 :
				break
		
		self.assertEqual( r , 404 )
