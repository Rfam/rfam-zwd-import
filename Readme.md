
# Code for importing Zasha Weinberg Database into RNAcentral

## Running with Docker

```
docker build -t zwd2rnacentral .
docker run -v `pwd`:/data/rnacentral -it zwd2rnacentral bash
python rnacentral/zasha2rnacentral.py
cd rnacentral-data-schema && python2 validate.py /data/rnacentral/zwd.json
```
