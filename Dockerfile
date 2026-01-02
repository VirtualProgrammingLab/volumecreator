FROM python:3.14-alpine

LABEL maintainer="pascal.seeland@tik.uni-stuttgart.de"

WORKDIR /

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


RUN mkdir /tmp/shared
COPY src/volumecreator.py /


ENV PYHTONPATH /
ENV FLASK_APP volumecreator
ENV FLASK_ENV development

EXPOSE 5000
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]
