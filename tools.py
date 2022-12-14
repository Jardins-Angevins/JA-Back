import numpy as np
import base64


def base64_to_numpy(image_base64,width,height):
	image = np.frombuffer(base64.b64decode(bytes(image_base64,"utf-8")), dtype=np.uint8)
	return np.reshape(image,(1,width,height,3))