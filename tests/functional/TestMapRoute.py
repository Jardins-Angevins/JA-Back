import unittest
import requests
import json

BASE_URL = 'http://localhost:8088/map'

class TestStatisticsRoute(unittest.TestCase):

	def test_fetch(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":49,"long":0,"dlat":10,"dlong":10} )
		data = json.loads( response.text )
		self.assertEqual( response.status_code , 200 )
		self.assertIsInstance( data['inputs'] , list )
		self.assertEqual( len(data['inputs']) , 4 )
		self.assertIsInstance( len(data['inputs'][0]['latitude']) , float )
		self.assertIsInstance( len(data['inputs'][0]['longitude']) , float )
		self.assertIsInstance( len(data['inputs'][0]['iaGuessedSpeciesId']) , int )


	# Missing mandatory args
	def test_missing_mandatory_arg_lat(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"long":0,"dlat":10,"dlong":10} )
		self.assertEqual( response.status_code , 400 )

	def test_missing_mandatory_arg_long(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":49,"dlat":10,"dlong":10} )
		self.assertEqual( response.status_code , 400 )

	def test_missing_mandatory_arg_dlat(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":49,"long":0,"dlong":10} )
		self.assertEqual( response.status_code , 400 )

	def test_missing_mandatory_arg_dlong(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":49,"long":0,"dlat":10} )
		self.assertEqual( response.status_code , 400 )


	# Wrong type for mandatory args
	def test_wrong_type_on_arg_lat(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":"nope","long":0,"dlat":10,"dlong":10} )
		self.assertEqual( response.status_code , 400 )

	def test_wrong_type_on_arg_long(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"long":"nope","lat":49,"dlat":10,"dlong":10} )
		self.assertEqual( response.status_code , 400 )

	def test_wrong_type_on_arg_dlat(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"dlat":"nope","lat":49,"long":0,"dlong":10} )
		self.assertEqual( response.status_code , 400 )

	def test_wrong_type_on_arg_dlong(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"dlong":"nope","lat":49,"long":0,"dlat":10} )
		self.assertEqual( response.status_code , 400 )


	# Wrong type for optionnal args
	def test_wrong_type_on_arg_year(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":49,"long":0,"dlat":10,"dlong":10,"year":"n"} )
		self.assertEqual( response.status_code , 400 )

	def test_wrong_type_on_arg_species(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":49,"long":0,"dlat":10,"dlong":10,"species":"n"} )
		self.assertEqual( response.status_code , 400 )


	# Special value which could make a crash
	def test_special_value_for_arg_year(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":49,"long":0,"dlat":10,"dlong":10,"year":-99999} )
		self.assertEqual( 400 )

	def test_special_value_for_arg_species(self):
		response = requests.post( BASE_URL , json={'image64' : self.correctImage},params={"lat":49,"long":0,"dlat":10,"dlong":10,"species":-99999} )
		self.assertEqual( 400 )

	# Verify filters
	### Year
	### Species


	# Verify security
	### 416 in case of too wide area

	
