import csv
import os.path
import re
import threading
import urllib.request
import cv2
import requests
from tqdm import tqdm

import sys
sys.path.append('.')
from config import config

PATH_CSV =          config.get('IA.Model.PATH_CSV')
DATAS_PATH =        config.get('IA.Model.DATAS_PATH')
TELA_IMAGE_FORMAT = config.get('Scraping.TELA_IMAGE_FORMAT')

"""
N.B : This script used to download all images for each species of the csv file.
"""

illustrations = 'https://www.tela-botanica.org/bdtfx-nn-%s-illustrations'

start = 0
end = None # to specify the start and the end of the csv file
species_to_get = None # to specify species in a list
max_thread = 5

LOCK = threading.Lock()

seuil_image_size = 24
def is_bad_image(file_name):
    image = cv2.imread(file_name)
    bad_image = (image.shape[0] < seuil_image_size and image.shape[1] < seuil_image_size) \
                or image is None
    with open(os.path.join(file_name), 'rb') as f:
        check_chars = f.read()[-2:]
        check_bad_image = bad_image or (check_chars != b'\xff\xd9')
    return bad_image

def get_image_by_num(num):
    global progressbar, total_size , total_download
    try:
        response = requests.get(illustrations % num)
    except Exception as e:
        print(e)
        return
    all_name = re.findall(r'https://api\.tela-botanica\.org/img:([0-9]+).*', response.text)
    all_name = set([f"{name}{TELA_IMAGE_FORMAT}.jpg" for name in all_name])
    for name in all_name:
        file_name = f'{DATAS_PATH}/IMG_{num}_{name}'
        if os.path.exists(file_name):
            if is_bad_image(file_name):
                os.remove(file_name)
                print("Bad image: Delete file")
        else :
            try:
                urllib.request.urlretrieve(f"https://api.tela-botanica.org/img:{name}", file_name)
                if os.path.exists(file_name) and is_bad_image(file_name):
                    os.remove(file_name)
                    print("Bad image in download: Delete file")
                else:
                    with LOCK:
                        total_download += os.stat(file_name).st_size
            except Exception as e:
                print(e)
                return
        with LOCK:
            progressbar.set_description(f'Volume de donées total : {round(total_size / 1048576,2)} Mo | Volume téléchargé : {round(total_download/1048576,2)} Mo | Progression totale')
            if os.path.exists(file_name):
                total_size += os.stat(file_name).st_size

    with LOCK:
        progressbar.update()

if species_to_get is not None:
    num_list = species_to_get
else :
    with open(PATH_CSV, newline='') as csvfile:
        csv_list = list(csv.reader(csvfile, delimiter=','))[1:]
        num_list = list(set([list(line)[3] for line in csv_list if list(line)[3].isdigit()]))
        num_list.sort()
        num_list = num_list[start:end]


print("Numéro taxonimique des espèce à télécharger :",num_list)

total_size = 0
total_download = 0
threads = []
progressbar = tqdm(desc=f'Volume de donées total : {total_size / 10E6} | Volume téléchargé : {round(total_download/1048576,2)} Mo | Progression totale', total=len(num_list))

for num in num_list:
    thread = threading.Thread(target=get_image_by_num, args=[num])
    thread.start()
    threads.append(thread)
    while len(threads) > max_thread:
        threads.pop(0).join()

for thread in threads:
    thread.join()

progressbar.set_description(
    f'Volume de donées total : {round(total_size / 1048576, 2)} Mo | Volume téléchargé : {round(total_download / 1048576, 2)} Mo | Progression totale')