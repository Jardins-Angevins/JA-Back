
global config


from flask import Flask

from tools import base64_to_numpy
from flask import request

from ia.model_loader import Model
import services.stats as statsService 
import services.db as dbService

import json

from config import config

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

	if dlat*dlong > 6:
		return {},416

	if (year != None) and (year < 0):
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
	# TODO : Set a limit rate on this query to avoid some kind of denial service attacks or saturation of the storage space of the database 
	lat = request.args.get('lat')
	long = request.args.get('long')

	# Check request validity
	## Mandatory args
	if any( x==None for x in [lat,long] ):
		return {},400
	## Check type
	try:
		lat  = float(lat)
		long  = float(long)
	except ValueError:
		return {},400

	# Handle request body
	## Extract
	data = request.get_json()
	## Image must have been transfered
	if not ("image64" in data):
		return {},400
	image_base64 = data["image64"]
	## Reshape
	try:
		image = base64_to_numpy(image_base64)
	except AttributeError:
		# If unable to reshape : image have been given in wrong format or ratio
		return {},400
	except ValueError:
		# If unable to reshape : image have been given in wrong format or ratio
		return {},400

	# logic
	## Predict
	predict,predictionList = model.predict_one(image)
	predict = int(predict)
	## Save entry into the database
	dbService.addInput(image_base64,predict,lat,long,predictionList)
	## Send response
	return json.dumps({
		"prediction": predict
	}),201


@app.route('/species', methods=['GET'])
def species():
	nominal_number = request.args.get('nominalNumber')

	# Check request validity
	## Mandatory args
	if any( x==None for x in [nominal_number] ):
		return {},400
	## Check type
	try:
		nominal_number  = int(nominal_number)
	except ValueError:
		return {},400

	# logic
	species = dbService.getOneSpecies(nominal_number)
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
app.run(
	debug=config.get('WEB.DEBUG'),
	port=config.get('WEB.PORT'),
	host='0.0.0.0'
)