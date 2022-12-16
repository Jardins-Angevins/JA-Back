FROM python:3.10-bullseye

ENTRYPOINT /bin/bash

WORKDIR /var/Jardins-Angevins

RUN apt update -q -y
RUN apt install ffmpeg libsm6 libxext6 -q -y

USER mathias

RUN pip3 install numpy scikit-learn requests keras autokeras flask cassandra-driver opencv-python tqdm

ENTRYPOINT python3



