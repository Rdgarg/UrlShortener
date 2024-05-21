# syntax=docker/dockerfile:1

FROM python:3.8-slim-bullseye

WORKDIR /

EXPOSE 5000

RUN apt-get update --yes && apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config --yes
#RUN apt-get update --yes && apt-get install pkg-config --yes
#export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags`
#export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

#CMD ["flask","--app", "run", "--host=0.0.0.0"]