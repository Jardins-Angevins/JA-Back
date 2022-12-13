import csv
import base64
import numpy as np
from flask import Flask, request,abort
from keras.models import load_model
import autokeras as ak

app = Flask(__name__)

PATH_CSV = "/home/etud/PycharmProjects/JA-Angers/datas/tela_botanica_export.csv"
IMAGE_SIZE = 256

loaded_model = load_model("model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)
with open(PATH_CSV, newline='') as csvfile:
    csv_list = list(csv.reader(csvfile, delimiter=','))[1:]
    label_list = list(set([list(line)[3] for line in csv_list if list(line)[3].isdigit()]))
    label_list.sort()


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    image_base64 = request.get_json()["image64"]
    image = np.frombuffer(base64.b64decode(bytes(image_base64,"utf-8")), dtype=np.uint8)
    image = np.reshape(image,(1,IMAGE_SIZE,IMAGE_SIZE,3))
    prediction = loaded_model.predict(image)[0]
    maximum = np.where(prediction == np.max(prediction))[0][0]
    resp = label_list[maximum]
    print(resp)
    return resp

if __name__ == '__main__':
    app.run(debug=True)