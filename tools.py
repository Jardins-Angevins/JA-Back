from PIL import Image
from io import BytesIO
import base64
import numpy as np

from config import config

def base64_to_numpy(image_base64):
	width,height = config.get('IA.IMAGE_SIZE')
	# Parse image from b64 png RGB
	image = np.array( Image.open(BytesIO(base64.b64decode(image_base64))) )
	# Check if image is at least near to the correct dimensions
	w,h,c = image.shape
	if abs(width - w) > 5 or abs(height - h) > 5 or (c != 3 and c != 4):
		raise ValueError()
	# If it is not exactly what we ask add black border
	if w != width or h != height:
		result = np.zeros( (width,height,3) )
		result[ :min(w,width) , :min(h,height) , 0:3 ] = image[ :min(w,width) , :min(h,height) , 0:3 ]
		return result
	else:
		return image