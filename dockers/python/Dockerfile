FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-pip

#RUN pip install -r /requirements.txt
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Para corregir problemas con el encoding
RUN export PYTHONIOENCODING=utf-8

WORKDIR /root
