#!/usr/bin/env python3
import argparse
import json
import sys

from variantapi.client import VariantAPIClient

__author__ = 'ckopanos, Leopold von Seckendorff'

def create_parser():
    """arguments are parsed in separate function for testing"""

    parser = argparse.ArgumentParser(
        description='CLI Utility for Varsome API. You can either input '
            'variants directly using -q, or define an input CSV file '
            'using -f. Results are returned to STDOUT. To save output '
            'to file, use a pipe ( > output.json)')
    parser.add_argument(
        '-k',
        # '--api_key',
        help='Your key to the API',
        type=str,
        metavar='API Key',
        required=False
        )
    parser.add_argument(
        '-g',
        # '--ref_genome',
        help='Reference genome either hg19 or hg38',
        type=str,
        metavar='Reference Genome',
        required=False,
        default=None
        )
    parser.add_argument(
        '-p',
        # '--parameters',
        help='Request parameters '
            'e.g. add-all-data=1 expand-pubmed-articles=0',
        type=str,
        metavar='params',
        required=False,
        nargs='+'
        )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-q',
        # '--query',
        help='Query to lookup in the API e.g. chr19:20082943:1:G '
            'or in case of batch request '
            'e.g. chr19:20082943:1:G rs113488022',
        type=str,
        metavar='variants',
        nargs='+'
        )
    group.add_argument(
        '-f',
        # '--input-file',
        help='Path to csv file with variants. It should include '
            'one variant per line.',
        type=str,
        metavar='Input CSV File',
        )
    
    return parser

def main():

    parser = create_parser()
    parser.parse_args()

    api_key = args.k
    query = args.q
    ref_genome = args.g
    if args.p:
        request_parameters = {
            param[0]: param[1] for param in [
                param.split('=') for param in args.p
                ]
            }
    else:
        request_parameters = None

    api = VariantAPIClient(api_key)

    if len(query) == 1:
        result = api.lookup(
                    query[0],
                    params=request_parameters,
                    ref_genome=ref_genome
                    )
    else:
        if api_key is None:
            sys.exit(
                'You need to pass an api key to perform batch requests. '
                'consider using batchRequestClient.py for large batch lookups'
                )
        result = api.batch_lookup(
                    query,
                    params=request_parameters,
                    ref_genome=ref_genome
                    )

    if result:
        print(json.dumps(result, indent=4, sort_keys=True))
    else:
        print('No result')

if __name__ == '__main__':
    main()
