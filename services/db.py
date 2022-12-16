from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine.management import create_keyspace_simple 
from cassandra.cqlengine.management import sync_type, sync_table
from cassandra.util import uuid_from_time
from cassandra.cluster import Cluster

import time
###
### Connexion to database
###

connection.setup( hosts=['database'] , default_keyspace='JardinsAngevins' )
create_keyspace_simple( name = 'JardinsAngevins', replication_factor = 1 )

###
### Models
###

class Stats(UserType):
	water        = columns.SmallInt()
	light        = columns.SmallInt()
	toxicity     = columns.SmallInt()

class Species(Model):
	nominalNumber      = columns.BigInt(primary_key=True)
	name               = columns.Text()
	scientificName     = columns.Text()
	refImage           = columns.Ascii() #Base64 Image
	stats              = columns.UserDefinedType(Stats)
	images             = columns.List( value_type = columns.Ascii ) #Base64 Image

class Probability(UserType):
	speciesId = columns.UUID() #Foreign jey of Species id
	trust = columns.Float()

class UserInput(Model):
	id                 = columns.UUID(primary_key=True)
	image              = columns.Ascii() #Base64 Image
	iaGuessedSpeciesId = columns.BigInt() #Foreign key of Species.id
	iaGuesses          = columns.List( value_type = columns.UserDefinedType(Probability) )
	latitude           = columns.Float()
	longitude          = columns.Float()
	photoTimestamp     = columns.Integer()
	


sync_type ( 'JardinsAngevins', Stats )
sync_type ( 'JardinsAngevins', Probability )
sync_table ( Species )
sync_table ( UserInput )

# Define here method to fetch database using :
# - https://cassandra.apache.org/_/quickstart.html
# - https://docs.datastax.com/en/developer/python-driver/3.25/getting_started/#executing-queries
# - https://docs.datastax.com/en/developer/python-driver/3.25/cqlengine/queryset/

def getUUID():
	return uuid_from_time(time.time())
	
def getAllSpecies():
	return Species.objects.all()

def getContributionCount():
	return UserInput.objects.count()

def getSpeciesCount():
	return Species.objects.count()
	
def getPlantsCount():
	return UserInput.objects.count()

def getPictureCount():
	# Implement logic : count(UserInput) + ( foreach k in Species count(images) )
	return UserInput.objects.count() + sum( [ len( species.images ) for species in Species.objects.all() ] )
	# /!\ WARNING TODO this is an inneficient way of doing this because all() as an LIMIT attribute in the query and the logic for the Species part should be done by Cassandra
	# /!\ WARNING TODO however CQL does not support subquery technic so we can't use method like SELECT COUNT(x) FROM ( SELECT COUNT(images) FROM Species GROUP BY Id ) 
	# /!\ WARNING TODO and there is no such method len() of List to make a query like : SELECT SUM(LEN(images)) FROM Species WHERE id = 1; 

def getOneSpecies(nominalNumber):
	return Species.filter(nominalNumber=nominalNumber).first()

def getAllInputsInRange(firstposition,secondposition):
	# Implement logic : firstposition and secondposition represent a square we return the inputs inside this square
	latitudes = (firstposition[0],secondposition[0]) if firstposition[0] > secondposition[0] else (secondposition[0],firstposition[0])
	longitudes = (firstposition[1],secondposition[1]) if firstposition[1] > secondposition[1] else (secondposition[1],firstposition[1])
	inputs = UserInput.filter(latitude__gte=latitudes[1],latitude__lte=latitudes[0],longitude__gte=longitudes[1],longitude__lte=longitudes[0]).allow_filtering()
	# TODO : allow_filtering() is not efficiency in cassandra the other way use filter without allowing we can index latititude and longitude as primary keys
	return list(inputs)