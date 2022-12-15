from flask import Flask
from faker import fake
from db import getAllSpecies, getContributionCount

from tools import base64_to_numpy
from flask import request
from IA import Model

import services.stats as statsService 
import db

import json


app = Flask(__name__, instance_relative_config=True)

fake()



@app.route('/statistics', methods=['GET'])
def statistics():
	return json.dumps({
		'pictureCount': 0,
		'contributionCount': db.getContributionCount(),
		'downloadCount': statsService.getDownloadCount(),
		'speciesCount': 0,
		'plantsCount': 0
	})

@app.route('/map', methods=['GET'])
def map():
	return f"{[ x for x in db.getAllSpecies()]}"

@app.route('/query', methods=['POST'])
def query():
	# Extract
	data = request.get_json()
	image_base64 = data["image64"]
	# Reshape
	image = base64_to_numpy(image_base64,256,256)
	# Predict
	return Model.predict(image)
	# TODO : save query in DB

@app.route('/species', methods=['GET'])
def species():
	return ''

app.run(debug=True, port=8088, host='0.0.0.0')