import cv2
import os
import numpy as np
from tqdm import tqdm
import autokeras as ak

datas_path = '../datas/tela_botanica_images_min'


def reshape_img(img):
    if img.shape[0] > img.shape[1]:
        factor = 256 / img.shape[0]
        img = cv2.resize(img, (round(factor * img.shape[1]), 256))
    elif img.shape[1] > img.shape[0]:
        factor = 256 / img.shape[1]
        img = cv2.resize(img, (256, round(factor * img.shape[0])))
    else:
        img = cv2.resize(img, (256, 256))

    if img.shape[0] > 256:
        centerX = img.shape[0] // 2
        img = img[centerX - 128: centerX + 128]
    if img.shape[1] > 256:
        centerY = img.shape[1] // 2
        img = img[:, centerY - 128: centerY + 128]

    return cv2.resize(img, (256, 256))


def reshape_img2(img):
    if img.shape[0] > img.shape[1]:
        factor = 256 / img.shape[0]
        img = cv2.resize(img, (round(factor * img.shape[1]), 256))
    elif img.shape[1] > img.shape[0]:
        factor = 256 / img.shape[1]
        img = cv2.resize(img, (256, round(factor * img.shape[0])))
    else:
        img = cv2.resize(img, (256, 256))

    do_transpose = False
    if img.shape[1] < 256:
        img = img.transpose((1, 0, 2))
        do_transpose = True

    if img.shape[0] < 256:
        rest = 256 - img.shape[0]
        arr = np.array([[[0, 0, 0] for i in range(256)] for j in range(rest // 2)], dtype=np.uint8)
        arr2 = np.array([[[0, 0, 0] for i in range(256)] for j in
                         range((rest // 2) if (rest % 2 == 0) else (rest // 2) + 1)], dtype=np.uint8)
        img = np.concatenate((arr, img, arr2))

    if do_transpose:
        img = img.transpose((1, 0, 2))

    return img


def dataset_creator(datas_path):
    # Trouve toutes les photos et les redimensionne
    x_dataset = []
    y_dataset = []
    for file in tqdm(os.listdir(datas_path)):
        img = cv2.imread(f'{datas_path}/{file}')
        img = reshape_img2(img)

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
