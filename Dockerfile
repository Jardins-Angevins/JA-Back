FROM python:3.10-bullseye

ENTRYPOINT /bin/bash

WORKDIR /var/Jardins-Angevins

RUN pip3 install numpy scikit-learn requests keras autokeras flask cassandra-driver

ENTRYPOINT python3