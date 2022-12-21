import unittest
import requests
import json

BASE_URL = 'http://localhost:8088/map'

class TestStatisticsRoute(unittest.TestCase):

	def test_fetch(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":2,"dlong":2} )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 200 )
		self.assertIsInstance( data['inputs'] , list )
		self.assertEqual( len(data['inputs']) , 4 )
		self.assertIsInstance( data['inputs'][0]['latitude'] , float )
		self.assertIsInstance( data['inputs'][0]['longitude'] , float )
		self.assertIsInstance( data['inputs'][0]['iaGuessedSpeciesId'] , int )


	# Missing mandatory args
	def test_missing_mandatory_arg_lat(self):
		response = requests.get( BASE_URL , params={"long":0,"dlat":2,"dlong":2} )
		self.assertEqual( response.status_code , 400 )

	def test_missing_mandatory_arg_long(self):
		response = requests.get( BASE_URL , params={"lat":49,"dlat":2,"dlong":2} )
		self.assertEqual( response.status_code , 400 )

	def test_missing_mandatory_arg_dlat(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlong":2} )
		self.assertEqual( response.status_code , 400 )

	def test_missing_mandatory_arg_dlong(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":2} )
		self.assertEqual( response.status_code , 400 )


	# Wrong type for mandatory args
	def test_wrong_type_on_arg_lat(self):
		response = requests.get( BASE_URL , params={"lat":"nope","long":0,"dlat":2,"dlong":2} )
		self.assertEqual( response.status_code , 400 )

	def test_wrong_type_on_arg_long(self):
		response = requests.get( BASE_URL , params={"long":"nope","lat":49,"dlat":2,"dlong":2} )
		self.assertEqual( response.status_code , 400 )

	def test_wrong_type_on_arg_dlat(self):
		response = requests.get( BASE_URL , params={"dlat":"nope","lat":49,"long":0,"dlong":2} )

	def test_wrong_type_on_arg_dlong(self):
		response = requests.get( BASE_URL , params={"dlong":"nope","lat":49,"long":0,"dlat":2} )
		self.assertEqual( response.status_code , 400 )


	# Wrong type for optionnal args
	def test_wrong_type_on_arg_year(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":2,"dlong":2,"year":"n"} )
		self.assertEqual( response.status_code , 400 )

	def test_wrong_type_on_arg_species(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":2,"dlong":2,"species":"n"} )
		self.assertEqual( response.status_code , 400 )


	# Special value which could make a crash
	def test_special_value_for_arg_year(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":2,"dlong":2,"year":-99999} )
		self.assertEqual( response.status_code , 400 )

	def test_special_value_for_arg_species(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":2,"dlong":2,"species":-99999} )
		self.assertEqual( response.status_code , 400 )


	# Verify filters
	def test_filter_year(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":2,"dlong":2,"year":2021} )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 200 )
		self.assertIsInstance( data['inputs'] , list )
		self.assertEqual( len(data['inputs']) , 1 )
		self.assertEqual( data['inputs'][0]['iaGuessedSpeciesId'] , 234567 )

	def test_filter_species(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":2,"dlong":2,"species":234567} )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 200 )
		self.assertIsInstance( data['inputs'] , list )
		self.assertEqual( len(data['inputs']) , 2 )
		self.assertEqual( data['inputs'][0]['iaGuessedSpeciesId'] , 234567 )
		self.assertEqual( data['inputs'][1]['iaGuessedSpeciesId'] , 234567 )

	def test_filter_year_and_species(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":2,"dlong":2,"species":234567,"year":2022} )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 200 )
		self.assertIsInstance( data['inputs'] , list )
		self.assertEqual( len(data['inputs']) , 1 )
		self.assertEqual( data['inputs'][0]['iaGuessedSpeciesId'] , 234567 )

	# Verify security
	def test_too_wide_area(self):
		response = requests.get( BASE_URL , params={"lat":49,"long":0,"dlat":10,"dlong":10} )
		self.assertEqual( response.status_code , 416 )

	
