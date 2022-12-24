import numpy as np
import base64

from config import config

def base64_to_numpy(image_base64):
	width,height = config.get('IA.IMAGE_SIZE')
	image = np.frombuffer(base64.b64decode(bytes(image_base64,"utf-8")), dtype=np.uint8)
	return np.reshape(image,(width,height,3))