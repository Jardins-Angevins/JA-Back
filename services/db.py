import datetime

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
	species_refid = columns.BigInt() #Foreign key of Species id
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

def getSpeciesList(page :int): 
	# /!\ WARNING TODO this is an inneficient way of doing pagination
	# /!\ WARNING TODO this is made like that just because there isn't any implementation of an OFFSET in CQL
	page_size = 25
	offset = page*page_size

	result = []
	i = 0
	for s in Species.objects.all():
		if i >= offset:
			result.append(s)
		i += 1
		if i >= (page_size + offset):
			break

	return result

def getOneSpecies(nominalNumber):
	return Species.filter(nominalNumber=nominalNumber).first()

def getAllInputsInRange(centerPos :tuple,deltaPos :tuple,speciesId :int,year :int):
	# Implement logic : centerPos and deltaPos represent a square
	cplat,cplong = centerPos
	dplat,dplong = deltaPos
	min_latitude = cplat - dplat
	max_latitude = cplat + dplat
	min_longitude = cplong - dplong
	max_longitude = cplong + dplong
	if year != None:
		year_start = time.mktime(time.strptime(f"{year}-01-01 00:00:01", '%Y-%m-%d %H:%M:%S'))
		year_end = time.mktime(time.strptime(f"{year+1}-01-01 00:00:01", '%Y-%m-%d %H:%M:%S'))
		if speciesId != None:
			query = UserInput.filter(
				latitude__gte=min_latitude,
				latitude__lte=max_latitude,
				longitude__gte=min_longitude,
				longitude__lte=max_longitude,
				iaGuessedSpeciesId=speciesId,
				photoTimestamp__gte=year_start,
				photoTimestamp__lte=year_end)
		else:
			query = UserInput.filter(
				latitude__gte=min_latitude,
				latitude__lte=max_latitude,
				longitude__gte=min_longitude,
				longitude__lte=max_longitude,
				photoTimestamp__gte=year_start,
				photoTimestamp__lte=year_end)
	else:
		if speciesId != None:
			query = UserInput.filter(
				latitude__gte=min_latitude,
				latitude__lte=max_latitude,
				longitude__gte=min_longitude,
				longitude__lte=max_longitude,
				iaGuessedSpeciesId=speciesId)
		else:
			query = UserInput.filter(
				latitude__gte=min_latitude,
				latitude__lte=max_latitude,
				longitude__gte=min_longitude,
				longitude__lte=max_longitude)
	return query.allow_filtering()
	# TODO : allow_filtering() is not efficiency in cassandra the other way use filter without allowing we can index latititude and longitude as primary keys

def addInput(image,predict,latitude,longitude,pred_list):
	temp = UserInput(
		id=getUUID(),
		image=image,
		iaGuessedSpeciesId=predict,
		latitude =latitude,
		longitude=longitude,
		photoTimestamp= datetime.datetime.now().timestamp(),
		iaGuesses=[ Probability(species_refid=int(label) , trust=trust) for (label,trust) in pred_list ]
	)
	temp.save()