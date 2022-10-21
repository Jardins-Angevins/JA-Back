import cv2
import numpy as np


def img_crop(img, dim):
    print(img.shape)
    if (img.shape[0] / img.shape[1]) == (dim[0] / dim[1]):
        return cv2.resize(img, dim)

    lower_shape = 0 if img.shape[0] < img.shape[1] else 1
    greater_shape = (lower_shape - 1) * -1
    factor = dim[lower_shape] / img.shape[lower_shape]
    new_dim = (dim[lower_shape], round(img.shape[greater_shape] * factor))
    if lower_shape == 0:
        new_dim = new_dim[::-1]
    img = cv2.resize(img, new_dim)
    print(img.shape)
    if img.shape[0] > dim[0]:
        centerX = img.shape[0] // 2
        img = img[centerX - (dim[0] // 2): centerX + (dim[0] // 2), :]
    if img.shape[1] > dim[1]:
        centerY = img.shape[1] // 2
        img = img[:, centerY - (dim[1] // 2): centerY + (dim[1] // 2)]

    return img


def img_all_crop(img, dim):
    print(img.shape)
    if (img.shape[0] / img.shape[1]) == (dim[0] / dim[1]):
        return cv2.resize(img, dim)

    lower_shape = 0 if img.shape[0] < img.shape[1] else 1
    greater_shape = (lower_shape - 1) * -1
    factor = dim[lower_shape] / img.shape[lower_shape]
    new_dim = (dim[lower_shape], round(img.shape[greater_shape] * factor))
    if lower_shape == 0:
        new_dim = new_dim[::-1]
    img = cv2.resize(img, new_dim)

    imgs = []
    if img.shape[0] > dim[0]:
        n = img.shape / dim[0]
        for i in range(0, n):
            start = (dim[0] * i) - ((dim[0] * (i + 1)) - img.shape[0])
            end = (dim[0] * (i+1)) if ((dim[0] * (i+1)) > img.shape[0]) else img.shape[0]
            imgs.append(img[start:end])

    if img.shape[1] > dim[1]:
        centerY = img.shape[1] // 2
        img = img[:, centerY - (dim[1] // 2): centerY + (dim[1] // 2)]

    return img


def img_fill_black(img):
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
