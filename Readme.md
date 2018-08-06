
# Code for importing Zasha Weinberg Database into RNAcentral

## Running with Docker

```
docker build -t zwd2rnacentral .
docker run -v `pwd`:/data/rnacentral -it zwd2rnacentral /bin/bash
python zasha2rnacentral.py
python /data/rnacentral-data-schema/validate.py /data/rnacentral/zwd.json
```
