import os
import sys
sys.path.append('.')
sys.path.append('ia')

import numpy as np
import ia_tools as ia_tools
import resize_algorithm as re
import model_loader as model_loader
import shutil

from config import config
DATAS_PATH =         config.get('IA.Model.DATAS_PATH')
PATH_RESIZED_SAVE =  config.get('IA.Model.PATH_RESIZED_SAVE')
IMAGE_SIZE =         config.get('IA.IMAGE_SIZE')
MODEL_NAME_H5 =      config.get('IA.Model.MODEL_NAME_H5')
MODEL_NAME =         config.get('IA.Model.MODEL_NAME')

"""
N.B : This script was used to debug images that cause problems during training. 
It works like:
 For each "offset" species, train the model If this train generates an error, 
 it is displayed and save it to the Error.log file.
"""


dataset = ia_tools.resize_all_images(DATAS_PATH,PATH_RESIZED_SAVE,re.img_crop_all,IMAGE_SIZE)

dataset = np.array(dataset)
print(dataset.shape)
species = list(set(list(dataset[1])))

offset = 2

for i in range(0,len(species),offset):
    if os.path.exists(MODEL_NAME_H5):shutil.rmtree(MODEL_NAME_H5)
    if os.path.exists(MODEL_NAME): shutil.rmtree(MODEL_NAME)

    species_local =  species[i:i+offset]

    x_dataset = []
    y_dataset = []

    for i in range(len(dataset[0])):
        #print((dataset[1][i] in species_local),dataset[0][i],species_local)
        if dataset[1][i] in species_local:
            x_dataset.append(dataset[0][i])
            y_dataset.append(dataset[1][i])

    x_dataset = np.array(x_dataset)
    y_dataset = np.array(y_dataset)

    np.save(PATH_RESIZED_SAVE,np.array([x_dataset,y_dataset]))
    try:
        model_loader.Model()
    except Exception as e:
        print(e)
        print("error on species: ", species_local)
        with open("error.log","a") as f:
            f.write("error on species: "+str(species_local)+"\n")
    if os.path.exists(MODEL_NAME_H5):shutil.rmtree(MODEL_NAME_H5)
    if os.path.exists(MODEL_NAME): shutil.rmtree(MODEL_NAME)

np.save(PATH_RESIZED_SAVE,dataset)
