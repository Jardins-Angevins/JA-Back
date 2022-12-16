from flask import Flask

from tools import base64_to_numpy
from flask import request

from ia.model_loader import Model
import services.stats as statsService 
import services.db as dbService

import json


app = Flask(__name__, instance_relative_config=True)

@app.route('/statistics', methods=['GET'])
def statistics():
	return json.dumps({
		'pictureCount': dbService.getPictureCount(),
		'contributionCount': dbService.getContributionCount(),
		'downloadCount': statsService.getDownloadCount(),
		'speciesCount': dbService.getSpeciesCount(),
		'plantsCount': dbService.getPlantsCount()
	}),200

@app.route('/map', methods=['GET'])
def map():
	lat = request.args.get('lat')
	long = request.args.get('long')
	dlat = request.args.get('dlat')
	dlong = request.args.get('dlong')

	species = request.args.get('species')
	year = request.args.get('year')

	# Check request validity
	## Mandatory args
	if any( x==None for x in [lat,long,dlat,dlong] ):
		return {},400
	## Check type
	try:
		lat  = float(lat)
		long  = float(long)
		dlat  = float(dlat)
		dlong  = float(dlong)
		if year != None:
			year = int(year)
		if species != None:
			species = int(species)
	except ValueError:
		return {},400
	
	# Logic
	## Ask database
	inputs = dbService.getAllInputsInRange((lat,long),(dlat,dlong),species,year)
	## Reshape output
	response = []
	for input in inputs:

		response.append({
			"latitude":input.latitude,
			"longitude":input.longitude,
			"iaGuessedSpeciesId":input.iaGuessedSpeciesId,
		})
	## Send response
	return json.dumps({"inputs":response}),200


@app.route('/query', methods=['POST'])
def query():
	lat = request.args.get('lat')
	long = request.args.get('long')
	# Extract
	data = request.get_json()
	image_base64 = data["image64"]
	# Reshape
	image = base64_to_numpy(image_base64,256,256)
	# Predict
	predict =  model.predict_one(image)
	# Save into the database
	dbService.addInput(image_base64,predict,lat,long)
	return json.dumps({
		"prediction": predict
	}),201


@app.route('/species', methods=['GET'])
def species():
	nominal_number = request.args.get('nominalNumber')
	species = dbService.getOneSpecies(int(nominal_number))
	if species is not None:
		return json.dumps(
			{
				"name":species.name,
				"scientificName":species.scientificName,
				"refImage":species.refImage,
				"stats": {
					"water":species.stats.water,
					"light":species.stats.light,
					"toxicity":species.stats.toxicity,
				}
			}
		),200
	else :
		return {"message": "This nominal number is uknown"}, 404

model = Model()
app.run(debug=True, port=8088, host='0.0.0.0')