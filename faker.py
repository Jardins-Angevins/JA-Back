from services.db import Species, Stats,UserInput,getUUID
import datetime
import numpy as np
from PIL import Image
import urllib.request
from math import floor
import base64
from io import BytesIO

def reshape( img ):
  x,y,c = img.shape
  if x > y :
    d = (x - y) //2
    return img[ d:d+y , :: ]
  else :
    d = (y - x) //2
    return img[ :: , d:d+x ]

def rescale( img ):
   ow,oh,oc = img.shape
   rw,rh,rc = 256,256,3
   r = np.zeros( (rw,rh,rc) )
   for i in range(rw):
     for j in range(rh):
       for c in range(3):
         x = floor( ow*i/rw )
         y = floor( oh*j/rh )
         r[i][j][c] = img[ x , y , c ]
   return r

def toBase64ImgPng( img ):
	# Convert the matrix image to a PNG image
	png_image = Image.fromarray( img.astype(np.uint8) )
	# Save the PNG image to a buffer
	buffer = BytesIO()
	png_image.save(buffer, format='PNG')
	# Encode the image as a base64 string
	return base64.b64encode(buffer.getvalue()).decode('utf-8')

urllib.request.urlretrieve('https://upload.wikimedia.org/wikipedia/commons/a/a3/Hain_Eiche_Herbst_121696.jpg','/tmp/jardins_angevins_faker_chene.jpg')
urllib.request.urlretrieve('https://upload.wikimedia.org/wikipedia/commons/4/4d/Bouleau-cepee.jpg','/tmp/jardins_angevins_faker_bouleau.jpg')                                                                                
urllib.request.urlretrieve('https://upload.wikimedia.org/wikipedia/commons/9/93/Papaver_rhoeas_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-101.jpg','/tmp/jardins_angevins_faker_coquelicot.jpg')
urllib.request.urlretrieve('https://upload.wikimedia.org/wikipedia/commons/4/4d/Fagus_silvatica1.jpg','/tmp/jardins_angevins_faker_hetre.jpg')

chene_img =      toBase64ImgPng( rescale( reshape( np.array( Image.open('/tmp/jardins_angevins_faker_chene.jpg'      ) ) ) ) )
bouleau_img =    toBase64ImgPng( rescale( reshape( np.array( Image.open('/tmp/jardins_angevins_faker_bouleau.jpg'    ) ) ) ) )
coquelicot_img = toBase64ImgPng( rescale( reshape( np.array( Image.open('/tmp/jardins_angevins_faker_coquelicot.jpg' ) ) ) ) )
hetre_img =      toBase64ImgPng( rescale( reshape( np.array( Image.open('/tmp/jardins_angevins_faker_hetre.jpg'      ) ) ) ) )

Species.create( 
	nominalNumber	= 992501,
	name            = "Coquelicot",
	scientificName  = "Papaver rhoeas",
	refImage        = coquelicot_img ,
	stats           = Stats(
		water    = 2,
		light    = 3,
		toxicity = 4
	),
	images          = [coquelicot_img , coquelicot_img]
)
Species.create( 
	nominalNumber	= 123456,
	name            = "Hêtre",
	scientificName  = "Fagus sylvatica",
	refImage        = hetre_img,
	stats           = Stats(
		water    = 1,
		light    = 1,
		toxicity = 1
	),
	images          = [hetre_img,hetre_img,hetre_img]
)
Species.create( 
	nominalNumber	= 234567,
	name            = "Chêne",
	scientificName  = "Quercus",
	refImage        = chene_img,
	stats           = Stats(
		water    = 2,
		light    = 2,
		toxicity = 0
	),
	images          = [chene_img]
)
Species.create( 
	nominalNumber	= 345678,
	name            = "Bouleau",
	scientificName  = "Betula",
	refImage        = bouleau_img,
	stats           = Stats(
		water    = 1,
		light    = 1,
		toxicity = 0
	),
	images          = [bouleau_img,bouleau_img]
)

UserInput.create(
	id=getUUID(),
	image = "SomeFakeBase64Data1",
	iaGuessedSpeciesId = 992501,
	latitude = 3,
	longitude = 3,
	photoTimestamp = datetime.datetime.now().timestamp()
)
UserInput.create(

	id=getUUID(),
	image = "SomeFakeBase64Data2",
	iaGuessedSpeciesId = 123456,
	latitude = 47.4778386,
	longitude = -0.6023297,
	photoTimestamp = datetime.datetime.now().timestamp()

)
UserInput.create(

	id=getUUID(),
	image = "SomeFakeBase64Data3",
	iaGuessedSpeciesId = 234567,
	latitude = 47.4781353,
	longitude = -0.6034488,
	photoTimestamp = datetime.datetime.now().timestamp()

)
UserInput.create(

	id=getUUID(),
	image = "SomeFakeBase64Data4",
	iaGuessedSpeciesId = 345678,
	latitude = 47.4811123,
	longitude = -0.5914023,
	photoTimestamp = datetime.datetime.now().timestamp()

)
UserInput.create(

	id=getUUID(),
	image = "SomeFakeBase64Data5",
	iaGuessedSpeciesId = 234567,
	latitude = 47.4706698,
	longitude = -0.5847032,
	photoTimestamp = 1639471345 # 2021-12-14 09:42:25

)
