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
Species.create( 
	nominalNumber	= 132456,
	name            = "Hêtre",
	scientificName  = "Fagus sylvatica",
	refImage        = "SomeFakeBase64Data",
	stats           = Stats(
		water    = 1,
		light    = 1,
		toxicity = 1
	),
	images          = ['SomeFakeBase64Data','SomeFakeBase64Data','SomeFakeBase64Data']
)
Species.create( 
	nominalNumber	= 234567,
	name            = "Chêne",
	scientificName  = "Quercus",
	refImage        = "SomeFakeBase64Data",
	stats           = Stats(
		water    = 2,
		light    = 2,
		toxicity = 0
	),
	images          = ['SomeFakeBase64Data']
)
Species.create( 
	nominalNumber	= 345678,
	name            = "Bouleau",
	scientificName  = "Betula",
	refImage        = "SomeFakeBase64Data",
	stats           = Stats(
		water    = 1,
		light    = 1,
		toxicity = 0
	),
	images          = ['SomeFakeBase64Data','SomeFakeBase64Data']
)

UserInput.create(
	id=getUUID(),
	image = "SomeFakeBase64Data1",
	iaGuessedSpeciesId = 992501,
	latitude = 3,
	longitude = 3,
	photoTimestamp = datetime.datetime.now().timestamp()
)
UserInput.create(

	id=getUUID(),
	image = "SomeFakeBase64Data2",
	iaGuessedSpeciesId = 123456,
	latitude = 47.4778386,
	longitude = -0.6023297,
	photoTimestamp = datetime.datetime.now().timestamp()

)
UserInput.create(

	id=getUUID(),
	image = "SomeFakeBase64Data3",
	iaGuessedSpeciesId = 234567,
	latitude = 47.4781353,
	longitude = -0.6034488,
	photoTimestamp = datetime.datetime.now().timestamp()

)
UserInput.create(

	id=getUUID(),
	image = "SomeFakeBase64Data4",
	iaGuessedSpeciesId = 345678,
	latitude = 47.4811123,
	longitude = -0.5914023,
	photoTimestamp = datetime.datetime.now().timestamp()

)
UserInput.create(

	id=getUUID(),
	image = "SomeFakeBase64Data5",
	iaGuessedSpeciesId = 234567,
	latitude = 47.4706698,
	longitude = -0.5847032,
	photoTimestamp = 1639471345 # 2021-12-14 09:42:25

)
