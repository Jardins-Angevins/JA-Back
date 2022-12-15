from flask import Flask
from faker import fake

from tools import base64_to_numpy
from flask import request
from ia.model_loader import Model

import services.stats as statsService 
import services.db as dbService

import json


app = Flask(__name__, instance_relative_config=True)

fake()



@app.route('/statistics', methods=['GET'])
def statistics():
	return json.dumps({
		'pictureCount': dbService.getPictureCount(),
		'contributionCount': dbService.getContributionCount(),
		'downloadCount': statsService.getDownloadCount(),
		'speciesCount': dbService.getSpeciesCount(),
		'plantsCount': dbService.getPlantsCount()
	})

@app.route('/map', methods=['GET'])
def map():
	return f"{[ x for x in dbService.getAllSpecies()]}"

@app.route('/query', methods=['POST'])
def query():
	# Extract
	data = request.get_json()
	image_base64 = data["image64"]
	# Reshape
	image = base64_to_numpy(image_base64,256,256)
	# Predict
	return model.predict_one(image)
	# TODO : save query in DB

@app.route('/species', methods=['GET'])
def species():
	nominal_number = request.args.get('nominalNumber')
	species = dbService.getOneSpecies(int(nominal_number))
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
	)

model = Model()
app.run(debug=True, port=8088, host='0.0.0.0')