from services.db import Species, Stats,UserInput,getUUID
import datetime

Species.create( 
	nominalNumber	= 992501,
	name            = "Coquelicot",
	scientificName  = "Papaver rhoeas",
	refImage        = "SomeFakeBase64Data",
	stats           = Stats(
		water    = 2,
		light    = 3,
		toxicity = 4
	),
	images          = ['SomeFakeBase64Data','SomeFakeBase64Data']
)

UserInput.create(

	id=getUUID(),
	image = "SomeFakeBase64Data",
	iaGuessedSpeciesId = 992501,
	latitude = 3,
	longitude = 3,
	photoTimestamp = datetime.datetime.now().timestamp()

)
