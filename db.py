from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine.management import create_keyspace_simple 
from cassandra.cqlengine.management import sync_type, sync_table
from cassandra.util import uuid_from_time

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
	id                = columns.UUID(primary_key=True)
	name              = columns.Text()
	scientificName    = columns.Text()
	refImage          = columns.Ascii() #Base64 Image
	stats             = columns.UserDefinedType(Stats)
	images            = columns.List( value_type = columns.Ascii ) #Base64 Image

#sync_type ( 'Stats', Stats )
sync_table ( Species )

# Define here method to fetch database using :
# - https://cassandra.apache.org/_/quickstart.html
# - https://docs.datastax.com/en/developer/python-driver/3.25/getting_started/#executing-queries
# - https://docs.datastax.com/en/developer/python-driver/3.25/cqlengine/queryset/

def getUUID():
	return uuid_from_time(time.time())
	
def getAllSpecies():
	return Species.objects.all()
