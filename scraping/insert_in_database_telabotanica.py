import os.path

import requests
from bs4 import BeautifulSoup
import re
import numpy
from PIL import Image
import base64
import csv
import warnings
import numpy as np
from multiprocessing import Pool
import multiprocessing
import tqdm

import sys
sys.path.append('.')
from config import config
from services.db import Species, Stats
from ia import resize_algorithm as ra

PATH_CSV =      config.get('IA.Model.PATH_CSV')
DATAS_PATH =    config.get('IA.Model.DATAS_PATH')
IMAGE_SIZE =    config.get('IA.IMAGE_SIZE')

start = 0
end = 3 # to specify the start and the end of the csv file
species_to_get = None # to specify species in a list

if species_to_get is None:
    with open(PATH_CSV, newline='') as csvfile:
        csv_list = list(csv.reader(csvfile, delimiter=','))[1:]
        species = list(set([list(line)[3] for line in csv_list if list(line)[3].isdigit()]))
        species.sort()
        species = species[start:end]
else:
    species = species_to_get


class Page_loader:
    SYNTHESE = "https://www.tela-botanica.org/bdtfx-nn-%s-synthese"
    def __init__(self):
        self.num = None
        self.load_synthese = None
        self.load_graph = None

    def _soup(self,num,url,builder):
        if num != self.num:

            self.num = num
            del self.load_graph
            del self.load_synthese
            self.load_graph = None
            self.load_synthese = None

            response = requests.get(url % self.num)
            soup = BeautifulSoup(response.content,builder)

            return soup

        return None

    def soup_synthese(self,num):
        soup = self._soup(num, Page_loader.SYNTHESE, "html.parser")

        if soup is None and self.load_synthese is not None:
            return self.load_synthese

        self.load_synthese = soup
        return soup


    def soup_graph(self,num):
        soup_synthese = self.soup_synthese(num)
        err = False
        try:
            graphique = soup_synthese.find(class_="svg")
            link = graphique.get("data")
        except:
            err = True
            return None
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'xml')
            return soup
        except:
            if not err: raise Exception("Here")

def get_lux(num,loader):
    soup = loader.soup_graph(num)
    try:
        lux_field = soup.find(id="ve_lumiere")
        lux = int(re.findall(r'.*\(([0-9 ]*) lux\)',lux_field.get('title'))[0].replace(' ',''))
        return lux
    except:
        return None


def get_water(num):
    return 0

def get_toxicity(num):
    return 0

def load_image(name_file):
    image = numpy.array(Image.open(os.path.join(DATAS_PATH, name_file)))
    image = list(ra.img_crop(image, IMAGE_SIZE))[0]
    image = np.array(image)
    image = base64.b64encode(image).decode("utf-8")
    return image

def get_images(num,loader):
    soup = loader.soup_synthese(num)
    image_field = soup.find(class_='illustration_cel')
    image = None
    images = []
    try:
        image_src = image_field.get('src')
        id_image = re.findall(r'.*/img:([0-9]*).*',image_src)[0]
        ref_name_file = f'IMG_{num}_{id_image}O.jpg' # O for the original size of the image
        try:
            image = load_image(ref_name_file)
        except FileNotFoundError:
            warnings.warn(f'Ref images :{ref_name_file} not available locally for the specie {num}')

        names_files = [img for img in os.listdir(DATAS_PATH) if img.startswith(f'IMG_{num}') and img != ref_name_file]

        for img in names_files:
            try:
                images.append(load_image(img))
            except FileNotFoundError:
                warnings.warn(f'Images {img} not available locally for the specie {num}')

    except AttributeError:
        warnings.warn(f'No images for the specie {num} ')

    return image,images

def get_scientific_name(num,loader):
    soup = loader.soup_synthese(num)
    span = soup.find(class_ = "sci")
    scientific_name = span.text

    return scientific_name

def get_name(num,loader):
    soup = loader.soup_synthese(num)
    div = soup.find(class_="toc-title")
    name = list(div.children)[2].strip()
    start = name.find(":") + 1
    name = name[start:].strip()
    name  = None if name == '' else name
    return name




def get_data(num):
    page_loader = Page_loader()
    ref, images = get_images(num, page_loader)
    data = {
        'nominalNumber':int(num),
        'name':get_name(num, page_loader),
        'scientificName':get_scientific_name(num, page_loader),
        'refImage':ref,
        'stats': {
            'water':get_water(num),
            'light':get_lux(num, page_loader),
            'toxicity':get_toxicity(num),
        },
        'images':images
    }
    return data

tbar = tqdm.tqdm(total=len(species))
with Pool(processes=multiprocessing.cpu_count()) as pool:
    for data in tqdm.tqdm(pool.imap(get_data,species)):
        tbar.update(1)
        Species.create(
            nominalNumber=data['nominalNumber'],
            name=data['name'],
            scientificName=data['scientificName'],
            refImage=data['refImage'],
            stats=Stats(
                water=data['stats']['water'],
                light=data['stats']['light'],
                toxicity=data['stats']['toxicity']
            ),
            images=data['images']
        )

pool.join()




