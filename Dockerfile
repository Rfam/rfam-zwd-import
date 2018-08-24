FROM biopython/biopython:latest

RUN mkdir /data

WORKDIR /data

RUN apt-get update && apt-get install -y \
  python-virtualenv \
  python-pip

RUN git clone https://bitbucket.org/zashaw/zashaweinbergdata.git && \
    cd zashaweinbergdata && \
    git checkout ba3b34e5418b990a87595ba150865be4d1d0bd35

RUN git clone https://github.com/RNAcentral/rnacentral-data-schema.git && \
    cd rnacentral-data-schema && \
    git checkout ad6f6fbd9181ea70a21a03a41515d01e20dc831f && \
    pip install -r requirements.txt
