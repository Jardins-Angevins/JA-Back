import csv
import os.path
import re
import shutil
import threading

import requests
from tqdm import tqdm
import sys

path_csv = '../datas/tela_botanica_export.csv'
illustrations = 'https://www.tela-botanica.org/bdtfx-nn-%s-illustrations'
folder_output = '../../datas/tela_botanica_images'
start = 0

LOCK = threading.Lock()
sizes = {}


def get_image_by_id(num, name):
    global progressbar, total_size
    file_name = f'{folder_output}/IMG_{num}_{name}'
    if not os.path.exists(file_name):
        print(file_name)
        sys.stdout.flush()
        try:
            res = requests.get("https://api.tela-botanica.org/img:" + name, stream=True)
        except Exception as e:
            print(e)
            return

        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)

        else:
            print(f"\n erreur sur name : {name} | Code de status : {res.status_code}")
    with LOCK:
        progressbar.set_description(f'Volume de donées total : {total_size / 10E6} | Progression totale')
        total_size += os.stat(file_name).st_size

    sizes[num] -= 1
    if sizes[num] <= 0:
        progressbar.update()


with open(path_csv, newline='') as csvfile:
    csv_list = list(csv.reader(csvfile, delimiter=','))[1 + start:]
    total_size = 0
    num_list = list(set([list(line)[3] for line in csv_list]))
    num_list.sort()
    print(num_list[-5])
progressbar = tqdm(desc=f'Volume de donées total : {total_size / 10E6} | Progression totale', total=len(num_list))
threads = []
max_threads = 100
for num in num_list:
    if num.isdigit():
        try:
            response = requests.get(illustrations % num)
        except Exception as e:
            print(e)
            continue
        all_name = set(re.findall(r'https://api\.tela-botanica\.org/img:([0-9-A-Za-z]+\.[a-z]{3})', response.text))
        with LOCK:
            sizes[num] = len(all_name)
        for name in all_name:
            thread = threading.Thread(target=get_image_by_id, args=[num, name])
            thread.start()
            threads.append(thread)

            while len(threads) >= max_threads:
                threads.pop().join()

for thread in threads:
    thread.join()
