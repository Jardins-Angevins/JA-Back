import csv
import os
import shutil

path_csv = '../datas/tela_botanica_export.csv'
folder_output = '/home/etud/PycharmProjects/JA-Angers/datas/tela_botanica_images'
folder_min = '/home/etud/PycharmProjects/JA-Angers/datas/tela_botanica_images_min'
start = 0
end = 10

with open(path_csv, newline='') as csvfile:
    csv_list = list(csv.reader(csvfile, delimiter=','))[1:]
    total_size = 0
    num_list = list(set([list(line)[3] for line in csv_list if list(line)[3].isdigit()]))
    num_list.sort()
    num_list = num_list[start:end]
    print(num_list)
    for file_name in os.listdir(folder_output):
        if file_name.split("_")[1] in num_list:
            print(file_name.split("_")[1])
            shutil.copy(f"{folder_output}/{file_name}",f"{folder_min}/{file_name}")