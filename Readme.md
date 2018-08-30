
# Code for importing ZWD into RNAcentral

[ZWD](https://bitbucket.org/zashaw/zashaweinbergdata) (Zasha Weinberg Database) is a repository containing
the RNA motif alignments produced by [Zasha Weinberg](https://orcid.org/0000-0002-6681-3624).

Many sequences in ZWD alignments are from environmental samples and cannot
be included in [Rfam](http://rfam.org) seed alignments because they do not have
stable identifiers and NCBI taxids.

In order to include all sequences in Rfam seed alignments,
all ZWD sequences are first imported into RNAcentral to assign stable identifiers
and NCBI taxids using the code from this repository.

## Usage

```
# build Docker image
docker build -t zwd2rnacentral .

# run Docker container and mount the current directory inside the container
docker run -v `pwd`:/data/rnacentral -it zwd2rnacentral bash

# generate JSON file
cd /data/rnacentral && python zwd2rnacentral.py

# validate JSON file against RNAcentral schema
cd /data/rnacentral-data-schema && python2 validate.py /data/rnacentral/zwd.json
```

The mapping between the Rfam 14.0 families and ZWD can be found in this
[Google Doc](https://docs.google.com/spreadsheets/d/12eAoN1RB2MN_XOwZ7ph3TsdUOppffHInf3mp2xHTieA/edit?usp=sharing).
