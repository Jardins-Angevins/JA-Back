FROM python:3.10-bullseye

ENTRYPOINT /bin/bash

WORKDIR /var/Jardins-Angevins

RUN pip3 install numpy scikit-learn requests keras autokeras flask cassandra-driver opencv-python tqdm
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

ENTRYPOINT python3



