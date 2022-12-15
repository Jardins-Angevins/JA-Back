from services.db import Species, Stats, getUUID


def fake():
	temp = Species( 
		id				= getUUID(),
		name            = "Coquelicot",
		scientificName  = "Papaver rhoeas",
		refImage        = "SomeFakeBase64Data",
		stats           = Stats(
			water    = 2,
			light    = 3,
			toxicity = 4
		),
		images          = ['SomeFakeBase64Data']
	)
	temp.save()
