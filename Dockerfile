FROM python:3.8-alpine

LABEL maintainer="pascal.seeland@tik.uni-stuttgart.de"

WORKDIR /

COPY requirements.txt ./

#RUN apk add --no-cache libmagic cyrus-sasl openssl

#RUN apk add --no-cache --virtual .build-deps  \
#        gcc \
#       libffi-dev \
#        musl-dev \
#        openssl-dev \
#cyrus-sasl-dev\
        
#  &&  pip install --no-cache-dir -r requirements.txt \
#  &&   apk del --no-network .build-deps 

RUN pip install --no-cache-dir -r requirements.txt
COPY src/volumecreator.py /

RUN mkdir /tmp/volumecreatoruploads
ENV PYHTONPATH /
ENV FLASK_APP volumecreator
ENTRYPOINT [ "flask" ]

CMD [ "run" , "--host=0.0.0.0" ]
