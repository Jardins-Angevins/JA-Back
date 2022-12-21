import csv
import numpy as np
from ia.ia_tools import dataset_creator
from ia import resize_algorithm as ra
import autokeras as ak
import keras.models as km
import os

PATH_CSV =      globals()['config']['IA']['Model']['PATH_CSV']
DATAS_PATH =    globals()['config']['IA']['Model']['DATAS_PATH']
MODEL_NAME_H5 = globals()['config']['IA']['Model']['MODEL_NAME_H5']
MODEL_NAME =    globals()['config']['IA']['Model']['MODEL_NAME']
IMAGE_SIZE =    globals()['config']['IA']['IMAGE_SIZE']
SAVED_N_BEST =  globals()['config']['IA']['SAVED_N_BEST']

class Model:
	def __init__(self):
		if not Model._exist_model():
			self._generate_model()
		else:
			self._load_model()
		self._generate_labels()


	def predict_one(self,image):
		"""
		:param image: single image in numpy format
		:return: a tuple of two elements with :
			the first one : a string label that describes the species of the plant in the image
			the second one : a list of pair ( label , trust ) with the n best species
		"""
		image = np.reshape(image,(1,image.shape[0],image.shape[1],3))
		prediction = self._loaded_model.predict(image)[0]
		maximum = np.where(prediction == np.max(prediction))[0][0]
		bestLabel = self._label_list[maximum]
		bestsPredictionsIndex = np.argpartition( prediction , SAVED_N_BEST )[-SAVED_N_BEST:]
		bestsPredictions = [ (self._label_list[ pId ],prediction[ pId]) for pId in bestsPredictionsIndex ]
		return (bestLabel,bestsPredictions)

	def _generate_model(self,max_trials=1):
		# train the model
		X_train, X_test, y_train, y_test = dataset_creator(DATAS_PATH, ra.img_fill_black,IMAGE_SIZE)
		clf = ak.ImageClassifier(overwrite=True, max_trials=max_trials)
		clf.fit(
			X_train,
			y_train,
			validation_data=(X_test, y_test)
		)
		# save the model
		model = clf.export_model()
		try:
			model.save(MODEL_NAME, save_format="tf")
		except Exception:
			model.save(MODEL_NAME_H5)

	def _load_model(self):
		if os.path.exists(MODEL_NAME):
			self._loaded_model = km.load_model(MODEL_NAME, custom_objects=ak.CUSTOM_OBJECTS)
		else:
			self._loaded_model =  km.load_model(MODEL_NAME_H5)

	def _generate_labels(self):
		with open(PATH_CSV, newline='') as csvfile:
			csv_list = list(csv.reader(csvfile, delimiter=','))[1:]
			self._label_list = list(set([list(line)[3] for line in csv_list if list(line)[3].isdigit()]))
			self._label_list.sort()

	@staticmethod
	def _exist_model():
		print("MODEL :",os.path.exists(MODEL_NAME),os.path.exists(MODEL_NAME_H5))
		return os.path.exists(MODEL_NAME) or os.path.exists(MODEL_NAME_H5)






