import csv
import os.path
import re
import threading
import urllib.request

import requests
from tqdm import tqdm

path_csv = '../datas/tela_botanica_export.csv'
illustrations = 'https://www.tela-botanica.org/bdtfx-nn-%s-illustrations'
folder_output = '../datas/tela_botanica_images_min'
start = 0
end = 3
max_thread = 5

LOCK = threading.Lock()


def get_image_by_num(num):
    global progressbar, total_size , total_download
    try:
        response = requests.get(illustrations % num)
    except Exception as e:
        print(e)
        return
    all_name = set(re.findall(r'https://api\.tela-botanica\.org/img:([0-9-A-Za-z]+\.[a-z]{3})', response.text))
    for name in all_name:
        file_name = f'{folder_output}/IMG_{num}_{name}'
        if not os.path.exists(file_name):
            try:
                urllib.request.urlretrieve(f"https://api.tela-botanica.org/img:{name}", file_name)
            except Exception as e:
                print(e)
                return
        with LOCK:
            progressbar.set_description(f'Volume de donées total : {round(total_size / 1048576,2)} Mo | Volume téléchargé : {round(total_download/1048576,2)} Mo | Progression totale')
            total_size += os.stat(file_name).st_size

    with LOCK:
        progressbar.update()


with open(path_csv, newline='') as csvfile:
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
