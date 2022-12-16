FROM python:3.10-bullseye

ENTRYPOINT /bin/bash

WORKDIR /var/Jardins-Angevins

RUN apt update -q -y
RUN apt install ffmpeg libsm6 libxext6 -q -y

ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID mathias 
RUN useradd -m -u $UID -g $GID -s /bin/bash mathias

USER mathias

RUN echo "export PATH=/home/mathias/.local/bin:$PATH" >> /home/mathias/.bashrc
RUN pip3 install numpy scikit-learn requests keras autokeras flask cassandra-driver opencv-python tqdm

ENTRYPOINT python3



