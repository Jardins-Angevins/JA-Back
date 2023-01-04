import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def flatten_generator(dataX, dataY):
    """
    :param dataX: np array of list of images
    :param dataY: labels associated for each list
    :return: flat numpy array of image and the associated label
    """
    x_dataset = []
    y_dataset = []
    for i, generator in enumerate(dataX):
        for img in generator:
            x_dataset.append(img)
            y_dataset.append(dataY[i])
            if img.shape[0] != 256 or img.shape[1] != 256:
                print(img.shape)

    x_dataset,y_dataset= np.array(x_dataset),np.array(y_dataset)
    return x_dataset,y_dataset

def resize_all_images(datas_path,path_save,resize_function,image_size):
    """
    :param datas_path: folder path where images are saved.
    :param path_save: file where the resized numpy are saved.
    :param resize_function: function used to resize the image in the ia.resize_algorithm. These functions returns an image generator.
    :param image_size: The dimension needed for the images
    :return: numpy array of list of images and the labels associated for each list
    """
    x_dataset = []
    y_dataset = []
    if not os.path.exists(path_save):
        for file in tqdm(os.listdir(datas_path)):
            if file.startswith("IMG"):
                img = cv2.imread(f'{datas_path}/{file}')
                imgs = list(resize_function(img, (image_size[0], image_size[1])))
                x_dataset.append(imgs)
                y_dataset.append(int(file.split("_")[1]))

        np.save(path_save,[x_dataset,y_dataset],allow_pickle=True)
    else:
        dataset = np.load(path_save,allow_pickle=True)
        x_dataset = dataset[0]
        y_dataset = dataset[1]
    return x_dataset,y_dataset
def dataset_creator(datas_path,path_save,resize_function,image_size,test_size=0.15):
    """

    :param datas_path: folder path where images are saved.
    :param path_save: file where the resized numpy are saved.
    :param resize_function: function used to resize the image in the ia.resize_algorithm. These functions returns an image generator.
    :param image_size: dimension needed for the images.
    :param test_size: size of the dataset for test.
    :return: dataset for train and test.
    """
    # Trouve toutes les photos et les redimensionne
    x_dataset,y_dataset = resize_all_images(datas_path,path_save,resize_function,image_size)

    X_train, X_test, y_train, y_test = train_test_split(x_dataset, y_dataset, test_size=test_size, random_state=0)
    X_train, y_train = flatten_generator(X_train, y_train)
    X_test, y_test = flatten_generator(X_test, y_test)
    return X_train, X_test, y_train, y_test






