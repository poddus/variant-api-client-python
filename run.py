#!/usr/bin/env python3
import argparse
import json
import sys
import os

from variantapi.client import VariantAPIClient

__author__ = 'ckopanos, Leopold von Seckendorff'

def create_parser():
    """arguments are parsed in separate function for testing"""

    parser = argparse.ArgumentParser(
        description='CLI Utility for Varsome API. You can either input '
            'variants directly using -q, or define an input CSV file '
            'using -f (API Key required). Results are returned to STDOUT. '
            'To save output to file, use a pipe ( > output.json)'
            )
    parser.add_argument(
        '-k',
        # '--api_key',
        help='path to your API key file',
        type=str,
        metavar='path',
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
        '-s',
        # '--query',
        help='single variant to lookup in the API e.g. chr19:20082943:1:G. '
            'for multiple variants use -f',
        type=str,
        metavar='variant'
        )
    group.add_argument(
        '-f',
        # '--input-file',
        help='Path to file with variants with one variant per line.',
        type=str,
        metavar='Input File',
        )
    
    return parser

def parse_the_args(args):
    
    if not args.k:
        api_key = None
    elif not os.path.exists(args.k):
       raise FileNotFoundError('{} does not exist'.format(args.k))
    else:
        with open(args.k, 'r') as f:
            api_key = f.read()

    if args.p:
        request_parameters = {
            param[0]: param[1] for param in [
                param.split('=') for param in args.p
                ]
            }
    else:
        request_parameters = None

    if not args.f:
        file_input = None
    elif not os.path.exists(args.f):
        raise FileNotFoundError('{} does not exist'.format(args.f))
    else:
        with open(args.f, 'r') as f:
            file_input = f.readlines()

    return api_key, args.s, args.g, request_parameters, file_input

def main():

    parser = create_parser()
    args = parser.parse_args()

    (
    api_key,
    single,
    ref_genome,
    request_parameters,
    file_input
    ) = parse_the_args(args)

    api = VariantAPIClient(api_key)

    if single:
        result = api.lookup(
                    single,
                    params=request_parameters,
                    ref_genome=ref_genome
                    )
    elif file_input:
        if api_key is None:
            raise SystemExit(
                'You need to pass an api key to perform batch requests.'
                )
        result = api.batch_lookup(
                    file_input,
                    params=request_parameters,
                    ref_genome=ref_genome
                    )


    if result:
        print(json.dumps(result, indent=4, sort_keys=True))
    else:
        print('No result')

if __name__ == '__main__':
    main()
