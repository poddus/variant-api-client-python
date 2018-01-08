# Variant API Client

## A basic api client implementation for [api.varsome.com](https://api.varsome.com)

This client is still in beta but it is a good start to start playing around with the API.

### Installation

Either download clone the repository from github and place the variantapi package within your code, or do

```bash
    pip install https://github.com/saphetor/variant-api-client-python/archive/master.zip
```
to install the package into your environment.

### API Documentation

Please visit the [api documentation](http://docs.varsome.apiary.io) to find out how to use the api and which values the api provides as a response to lookup requests.

### How to get an API key

You generally are not required to have an api key to use the api, though the number of requests you will be able to issue will be throttled.

Additionally, you will not be able to perform batch requests without an API key.

To obtain an API key please [contact us](mailto:support@saphetor.com)

Store the API key in a file called `varsome_api_key` containing only the token and a newline.

### Using the client in your code

Using the api client is quite straightforward. Just install the api client package and from within your code use

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

if you have installed the variantapi packagage into your environment (either using pip or by moving the folder to the working directory), you can use `run.py`, and `simpleVCFClient.py` from the command line to fetch data.

### run.py
this script has two modes
* `-s` for single lookups
    * passing an api key is optional for this mode, variants are passed via the command line
* `-f` for batch lookups
    * passing an api key is required for this mode, variants are passed via an input file

The utility outputs results to STDOUT. You may save the results to a file by piping, i.e.
```bash
./run.py -s 'BRAF:V600E' > output.json
```

Run
```bash
./run.py -h
```
for a list of available options

#### Single Variants example

```bash
./run.py -g hg19 -s 'chr19:20082943:1:G' -p add-all-data=1
```

You may optionally pass an api key (using `-k`) to limit throttling.

#### Large Batches

When retrieving information for multiple variants, use the `-f` flag.
It accepts a text file with one variant per line and outputs a json file. e.g.

```bash
./run.py -k path_to_token_file -f vars.txt
```

Run
```bash
./batchRequestClient.py -h
```
for a list of available options

### simpleVCFClient
pass

## Reference
To view available request parameters (used in the params method parameter) refer to an example at [api.varsome.com](https://api.varsome.com) or
the [api documentation](http://docs.varsome.apiary.io).

To understand how annotation properties are included in the json response please refer to the relevant [schema](https://api.varsome.com/lookup/schema)

