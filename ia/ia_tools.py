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

def resize_all_images(datas_path,path_save,resize_function,image_size):
    x_dataset = []
    y_dataset = []
    if not os.path.exists(path_save):
        for file in tqdm(os.listdir(datas_path)):
            if file.startswith("IMG"):
                with open(os.path.join(datas_path, file), 'rb') as f:
                    check_chars = f.read()[-2:]
                if check_chars != b'\xff\xd9':
                    print('Not complete image')
                else:
                    img = cv2.imread(f'{datas_path}/{file}')
                    imgs = list(resize_function(img, (image_size[0], image_size[1])))
                    x_dataset.append(imgs)
                    y_dataset.append(int(file.split("_")[1]))
        x_dataset = np.array(x_dataset)
        y_dataset = np.array(y_dataset)
        np.save(path_save,np.array([x_dataset,y_dataset]),allow_pickle=True)
    else:
        dataset = np.load(path_save,allow_pickle=True)
        x_dataset = dataset[0]
        y_dataset = dataset[1]
    return x_dataset,y_dataset
def dataset_creator(datas_path,path_save,resize_function,image_size):
    # Trouve toutes les photos et les redimensionne
    x_dataset,y_dataset = resize_all_images(datas_path,path_save,resize_function,image_size)

    X_train, X_test, y_train, y_test = train_test_split(x_dataset, y_dataset, test_size=0.15, random_state=0)
    X_train, y_train = flatten_generator(X_train, y_train)
    X_test, y_test = flatten_generator(X_test, y_test)
    return X_train, X_test, y_train, y_test






