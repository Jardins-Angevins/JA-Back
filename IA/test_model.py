import shutil
import urllib

import autokeras as ak
import cv2
import numpy as np
from keras.models import load_model
import urllib.request
#link = 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fpybio.org%2F01%2FASTERA13.jpg&f=1&nofb=1&ipt=fdf7589ce21ec0f7c0122d7568a91143197dc16c04e6908df82f661f6724248b&ipo=images '


# link = "http://www.phytoimages.siu.edu/users/paraman1/8_3_13_1/Upload3Aug13b/405_Poaceae.jpg"

#link = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F3.bp.blogspot.com%2F-XaCKjnSvxts%2FT4bI-z9_MPI%2FAAAAAAAAVGQ%2FDzvVyU_7SV8%2Fs1600%2FPhalaris%2Bparadoxa%2BL.%2B-Poaceae%2B-%2B%2BScagliola%2Bsterile%2B(4).jpg&f=1&nofb=1&ipt=5b13bbd7d97663a3aa817fbc90862914b9203817efe01e7163236bdd8e53cdf6&ipo=images"

#link = "http://www.stridvall.se/flowers/albums/Asteraceae_2/AAAA9015.jpg"


temp_name = '.temp'

loaded_model = load_model("../model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)
test = urllib.request.urlretrieve(link, temp_name)
print(test)

img = cv2.imread(temp_name)
img = reshape_img2(img)
cv2.imshow('image window', img)

cv2.waitKey(0)
cv2.destroyAllWindows()

print(loaded_model.predict(np.array([img])))
