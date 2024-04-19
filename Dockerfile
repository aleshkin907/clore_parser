FROM python:3.12

RUN apt-get update
RUN apt-get -y install postgresql-client

RUN mkdir /clore_app

WORKDIR /clore_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


RUN chmod a+x docker/*.sh

# WORKDIR src

# CMD python main.py