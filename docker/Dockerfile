FROM python:3.7-stretch

RUN apt-get update && apt-get install -yq --fix-missing \
    python3-setuptools \
    python3-pip \
&& apt-get clean

RUN pip3 install --upgrade pip setuptools virtualenv

COPY ./requirements.txt /
RUN pip3 install -r requirements.txt

COPY ./configurer/ /srv/configurer/

WORKDIR /srv

ENTRYPOINT [ "python3", "-m", "configurer", "--source",  "/source", "--output", "/output", "--vars", "/vars/var_file"]
