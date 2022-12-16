import unittest
import requests
import json

BASE_URL = 'http://localhost:8088/statistics'

class TestStatisticsRoute(unittest.TestCase):

	def test_fetch(self):
		response = requests.get( BASE_URL )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 200 )
		self.assertIsInstance( data['pictureCount'] ,      int )
		self.assertIsInstance( data['contributionCount'] , int )
		self.assertIsInstance( data['downloadCount'] ,     str )
		self.assertIsInstance( data['speciesCount'] ,      int )
		self.assertIsInstance( data['plantsCount'] ,       int )




