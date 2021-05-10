FROM biopython/biopython:latest

RUN mkdir /data

WORKDIR /data

RUN apt-get update && apt-get install -y \
  python-virtualenv \
  python-pip

RUN git clone https://bitbucket.org/zashaw/zashaweinbergdata.git && \
    cd zashaweinbergdata && \
    git checkout 0957c3b2bf063cfe6abaa03e8b453c2856ad19c1

RUN git clone https://github.com/RNAcentral/rnacentral-data-schema.git && \
    cd rnacentral-data-schema && \
    git checkout d34dcc82b35d4b2d748bb6ae4f59e10519500bfe && \
    pip install -r requirements.txt
