FROM biopython/biopython:latest

RUN mkdir /data
RUN git clone https://bitbucket.org/zashaw/zashaweinbergdata.git /data/zashaweinbergdata && \
    cd /data/zashaweinbergdata && \
    git checkout ba3b34e5418b990a87595ba150865be4d1d0bd35
