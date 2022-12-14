import cv2
import numpy as np
from typing import Iterable


def img_crop(img: np.ndarray, dim: tuple[int, int]):
    if (img.shape[0] / img.shape[1]) == (dim[0] / dim[1]):
        yield cv2.resize(img, dim)

    lower_shape = 0 if img.shape[0] < img.shape[1] else 1
    greater_shape = 0 if img.shape[0] > img.shape[1] else 1
    factor = dim[lower_shape] / img.shape[lower_shape]
    new_dim = (dim[lower_shape], round(img.shape[greater_shape] * factor))

    if lower_shape == 0:
        new_dim = new_dim[::-1]

    img = cv2.resize(img, new_dim)

    if img.shape[0] > dim[0]:
        centerX = img.shape[0] // 2
        img = img[centerX - (dim[0] // 2): centerX + (dim[0] // 2), :]
    if img.shape[1] > dim[1]:
        centerY = img.shape[1] // 2
        img = img[:, centerY - (dim[1] // 2): centerY + (dim[1] // 2)]

    yield img


def img_crop_all(img: np.ndarray, dim: tuple[int, int]) :
    if (img.shape[0] / img.shape[1]) == (dim[0] / dim[1]):
        yield cv2.resize(img, dim)

    lower_shape = 0 if img.shape[0] < img.shape[1] else 1
    greater_shape = 0 if img.shape[0] > img.shape[1] else 1
    factor = dim[lower_shape] / img.shape[lower_shape]
    new_dim = (dim[lower_shape], round(img.shape[greater_shape] * factor))

    if lower_shape == 0:
        new_dim = new_dim[::-1]

    img = cv2.resize(img, new_dim)

    if img.shape[0] > dim[0]:
        centerX = img.shape[0] // 2
        yield img[centerX - (dim[0] // 2): centerX + (dim[0] // 2), :]
        offset = img[0:centerX].shape[0] - dim[0] if img[0:centerX].shape[0] > dim[0] else 0
        yield img[0 + offset: dim[0] + offset, :]
        yield img[-dim[0] - offset: offset if offset > 0 else None, :]
    elif img.shape[1] > dim[1]:
        centerY = img.shape[1] // 2
        yield img[:, centerY - (dim[1] // 2): centerY + (dim[1] // 2)]
        offset = img[:, 0:centerY].shape[1] - dim[1] if img[:, 0:centerY].shape[1] > dim[1] else 0
        yield img[:, 0 + offset: dim[1] + offset]
        yield img[:, -dim[1] - offset: (-offset) if offset > 0 else None]


def img_fill_black(img: np.ndarray, dim: tuple[int, int]) :
    if (img.shape[0] / img.shape[1]) == (dim[0] / dim[1]):
        yield cv2.resize(img, dim)

    lower_shape = 0 if img.shape[0] < img.shape[1] else 1
    greater_shape = 0 if img.shape[0] > img.shape[1] else 1
    factor = dim[greater_shape] / img.shape[greater_shape]
    new_dim = (dim[greater_shape], round(img.shape[lower_shape] * factor))

    if greater_shape == 0:
        new_dim = new_dim[::-1]

    img = cv2.resize(img, new_dim)

    do_transpose = False
    if img.shape[1] < dim[1]:
        img = img.transpose((1, 0, 2))
        do_transpose = True

    if img.shape[0] < dim[0]:
        lenght_dim = 1 if do_transpose else 0
        rest = dim[0] - img.shape[0]

        arr = np.array([[[0, 0, 0] for i in range(dim[lenght_dim])] for j in range(rest // 2)], dtype=np.uint8)
        arr2 = np.array([[[0, 0, 0] for i in range(dim[lenght_dim])] for j in
                         range((rest // 2) if (rest % 2 == 0) else (rest // 2) + 1)], dtype=np.uint8)
        img = np.concatenate((arr, img, arr2))

    if do_transpose:
        img = img.transpose((1, 0, 2))

    return img
