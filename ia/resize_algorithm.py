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
    """
    :param img: image in the numpy array format.
    :param dim: dimension needed
    :return: a generator of 3 images: crop the middle, the right of the middle and the left of the middle
    N.B : We have tested more than one resized algorithm, but this algorithm witch give better performance
    """

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
        offset = centerX - dim[0] if centerX > dim[0] else 0
        yield img[0 + offset: dim[0] + offset, :]
        yield img[-dim[0] - offset: -offset if offset > 0 else None, :]
    elif img.shape[1] > dim[1]:
        centerY = img.shape[1] // 2
        yield img[:, centerY - (dim[1] // 2): centerY + (dim[1] // 2)]
        offset = centerY - dim[1] if centerY > dim[1] else 0
        yield img[:, 0 + offset: dim[1] + offset]
        yield img[:, -dim[1] - offset: (-offset) if offset > 0 else None]


