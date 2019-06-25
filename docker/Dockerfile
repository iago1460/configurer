FROM python:3.7.3-alpine3.9

COPY ./requirements.txt /
RUN pip3 install -r requirements.txt

COPY ./configurer/ /srv/configurer/

WORKDIR /srv

ENTRYPOINT [ "python3", "-m", "configurer", "--source",  "/source", "--output", "/output", "--vars", "/vars/var_file"]
