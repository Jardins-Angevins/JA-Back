import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import autokeras as ak
import resize_algorithm as ra
import tensorflow as tf

datas_path = 'datas/tela_botanica_images_min'


def flatten_generator(dataX, dataY):
    x_dataset = []
    y_dataset = []
    for i, generator in enumerate(dataX):
        for img in generator:
            x_dataset.append(img)
            y_dataset.append(dataY[i])

            cv2.imshow('image window', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    return np.array(x_dataset), np.array(y_dataset)


def dataset_creator(datas_path,resize_function):
    # Trouve toutes les photos et les redimensionne
    x_dataset = []
    y_dataset = []
    for file in tqdm(os.listdir(datas_path)):
        img = cv2.imread(f'{datas_path}/{file}')
        imgs = resize_function(img, (256, 256))
        x_dataset.append(imgs)
        y_dataset.append(int(file.split("_")[1]))

    X_train, X_test, y_train, y_test = train_test_split(x_dataset, y_dataset, test_size=0.2, random_state=0)
    X_train, y_train = flatten_generator(X_train, y_train)
    X_test, y_test = flatten_generator(X_test, y_test)
    return X_train, X_test, y_train, y_test


X_train, X_test, y_train, y_test = dataset_creator(datas_path,ra.img_fill_black)

clf = ak.ImageClassifier(overwrite=True, max_trials=10)

# Entrainement
clf.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test)
)


# Save model
model = clf.export_model()
try:
    model.save("model_autokeras", save_format="tf")
except Exception:
    model.save("model_autokeras.h5")
