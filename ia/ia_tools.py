import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tqdm import tqdm




def flatten_generator(dataX, dataY):
    x_dataset = []
    y_dataset = []
    for i, generator in enumerate(dataX):
        for img in generator:
            x_dataset.append(img)
            y_dataset.append(dataY[i])
    return np.array(x_dataset), np.array(y_dataset)


def dataset_creator(datas_path,resize_function,image_size):
    # Trouve toutes les photos et les redimensionne
    x_dataset = []
    y_dataset = []
    for file in tqdm(os.listdir(datas_path)):
        if file.startswith("IMG"):
            img = cv2.imread(f'{datas_path}/{file}')
            imgs = list(resize_function(img, (image_size[0], image_size[1])))
            x_dataset.append(imgs)
            y_dataset.append(int(file.split("_")[1]))

    X_train, X_test, y_train, y_test = train_test_split(x_dataset, y_dataset, test_size=0.15, random_state=0)
    X_train, y_train = flatten_generator(X_train, y_train)
    X_test, y_test = flatten_generator(X_test, y_test)
    return X_train, X_test, y_train, y_test






