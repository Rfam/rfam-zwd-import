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
    git checkout 98ad1ec84dff861fd1bbc131e941574779cd0076 && \
    pip install -r requirements.txt
