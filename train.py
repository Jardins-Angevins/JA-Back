import cv2
import os
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import autokeras as ak

datas_path = 'datas/tela_botanica_images_min'


def dataset_creator(datas_path):
    # Trouve toutes les photos et les redimensionne
    x_dataset = []
    y_dataset = []
    for file in tqdm(os.listdir(datas_path)):
        img = cv2.imread(f'{datas_path}/{file}')
        img = cv2.resize(img, (224, 224))

        x_dataset.append(img)
        y_dataset.append(int(file.split("_")[1]))

    return np.array(x_dataset), np.array(y_dataset)


x_dataset, y_dataset = dataset_creator(datas_path)

# On sépare les images en jeu de test vs jeu d'entrainement
X_train, X_test, y_train, y_test = train_test_split(x_dataset, y_dataset, test_size=0.33, random_state=1)
clf = ak.ImageClassifier(overwrite=True, max_trials=1)


# Entrainement
clf.fit(
    x_dataset,
    y_dataset,
    validation_data=(X_test, y_test),
    epochs=10
)

# Evaluation du modèle
clf.evaluate(X_test, y_test)
