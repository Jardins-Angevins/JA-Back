from services.db import Species, Stats


def fake():
	temp = Species( 
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
	temp.save()
