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
	id                 = columns.UUID(primary_key=True)
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
	iaGuessedSpeciesId = columns.UUID() #Foreign key of Species.id
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
