import csv
import numpy as np
from flask import Flask, request,abort
from keras.models import load_model
import autokeras as ak
import os

PATH_CSV = "datas/tela_botanica_export.csv"
IMAGE_SIZE = 256

if not os.path.exists('model_autokeras'):
	print('Missing model')
	exit(1)

loaded_model = load_model("model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)
with open(PATH_CSV, newline='') as csvfile:
	csv_list = list(csv.reader(csvfile, delimiter=','))[1:]
	label_list = list(set([list(line)[3] for line in csv_list if list(line)[3].isdigit()]))
	label_list.sort()

####

class Model():

	@staticmethod
	def predict( image ):
		prediction = loaded_model.predict(image)[0]
		maximum = np.where(prediction == np.max(prediction))[0][0]
		return label_list[maximum]