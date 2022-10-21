import cv2
import os
import numpy as np
from tqdm import tqdm
import autokeras as ak
import resize_algorithm as ra
datas_path = '../datas/tela_botanica_images_min'


def dataset_creator(datas_path):
    # Trouve toutes les photos et les redimensionne
    x_dataset = []
    y_dataset = []
    for file in tqdm(os.listdir(datas_path)):
        img = cv2.imread(f'{datas_path}/{file}')
        img = ra.img_crop(img)

        x_dataset.append(img)
        y_dataset.append(int(file.split("_")[1]))

    return np.array(x_dataset), np.array(y_dataset)


x_dataset, y_dataset = dataset_creator(datas_path)
print(x_dataset)
print(y_dataset)

clf = ak.ImageClassifier(overwrite=True, max_trials=1)

# Entrainement
clf.fit(
    x_dataset,
    y_dataset,
    epochs=10
)
model = clf.export_model()

try:
    model.save("model_autokeras", save_format="tf")
except Exception:
    model.save("model_autokeras.h5")
