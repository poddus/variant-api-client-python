# Variant API Client

## A basic api client implementation for [api.varsome.com](https://api.varsome.com)

This client is still in beta but it is a good start to start playing around with the API.

### Installation

Either download clone the repository from github and place the variantapi package
within your code, or do

```bash
    pip install https://github.com/saphetor/variant-api-client-python/archive/master.zip
```
to install the package into your environment.

### API Documentation

Please visit the [api documentation](http://docs.varsome.apiary.io) to find out how to use the api and
which values the api provides as a response to lookup requests.

### How to get an API key

You generally are not required to have an api key to use the api, though the number of requests you will be able
to issue will be throttled.

Additionally, you will not be able to perform batch requests without an API key.

To obtain an API key please [contact us](mailto:support@saphetor.com)

### Using the client in your code

Using the api client is quite straightforward. Just install the api client package and from within
your code use

```python
from variantapi.client import VariantAPIClient

# api key is not required for single variant lookups
api_key = 'Your token'
api = VariantAPIClient(api_key)

# if you don't have an api key use
# api = VariantAPIClient()

# fetch information about a variant into a dictionary
result = api.lookup(
            'chr19:20082943:1:G',
            params={'add-source-databases': 'gnomad-exomes,refseq-transcripts'},
            ref_genome='hg19'
            )
# access results e.g. the transcripts of the variant
transcripts = result['refseq_transcripts']

# fetch information for multiple variants
variants = ['chr19:20082943:1:G','chr22:39777823::CAA']

# results will be an array of dictionaries
# an api key is required for this request
results = api.batch_lookup(
            variants,
            params={'add-source-databases': 'gnomad-exomes,gnomad-genomes'},
            ref_genome='hg19'
            )
```

## Example Command Line Usage

if you have installed the variantapi packagage into your environment (either using pip or by moving the folder to the working directory), you can use `smallRequestClient.py`, `batchRequestClient.py`, and `simpleVCFClient.py` from the command line to fetch data.

### Single Variants or Small Batches

```bash
./smallRequestClient.py -g hg19 -q 'chr19:20082943:1:G' -p add-all-data=1
```

You may pass more than one values after the -q argument that will make a batch request
to the API but you will need a token to do that e.g.

```bash
./smallRequestClient.py -k 'your token' -g hg19 -q 'rs113488022' 'chr19:20082943:1:G' -p add-source-databases=gnomad-exomes,gnomad-genomes
```

Run

```bash
./smallRequestClient.py -h
```

for a list of available options

### Large Batches

When retrieving information for large batches, it is better to use `batchRequestClient.py`.
It accepts a text file with one variant per line and outputs a json file. e.g.

```bash
./batchRequestClient.py -i vars.txt -o test.json -k 'your token' -n 10
```

Run

```bash
./batchRequestClient.py -h
```

for a list of available options

## Reference
To view available request parameters (used in the params method parameter) refer to an example at [api.varsome.com](https://api.varsome.com) or
the [api documentation](http://docs.varsome.apiary.io).

To understand how annotation properties are included in the json response please refer to the relevant [schema](https://api.varsome.com/lookup/schema)

