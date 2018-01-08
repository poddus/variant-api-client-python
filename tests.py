#!/usr/bin/env python3

import unittest
import logging
import json

from variantapi.client import VariantAPIClient
from variantapi.client import VarsomeHTTPError

from run import create_parser
from run import parse_the_args

__author__ = 'Leopold von Seckendorff'

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
    )

class TestClient(unittest.TestCase):

    def setUp(self):
        with open('./varsome_api_key', 'r') as f:
            self.key = f.readline().rstrip('\n')

        self.varsome_api_no_auth = VariantAPIClient()
        self.varsome_api = VariantAPIClient(self.key)

    def test_HTTP_error_handling(self):
        logging.info('testing HTTP Error Handling...')
        # don't pass API key to raise 401 Error
        with self.assertRaises(VarsomeHTTPError):
            self.varsome_api_no_auth.batch_lookup(['BRAF:V600E'])

    def test_schema(self):
        logging.info('testing lookup schema...')
        with open('./test_files/schema.json', 'r') as f:
            results = json.loads(f.read())
        self.assertEqual(
            self.varsome_api.schema(),
            results
            )

    def test_lookup(self):
        logging.info('testing lookups...')
        lookup_results = './test_files/lookup/'

        with open(lookup_results + '0.json', 'r') as f:
            result = json.load(f)
        self.assertEqual(
            self.varsome_api.lookup('10190091015942290001'),
            result
            )

        with open(lookup_results + '1.json', 'r') as f:
            result = json.load(f)
        self.assertEqual(
            self.varsome_api.lookup('rs113488022', ref_genome='hg38'),
            result
            )
        with open(lookup_results + '2.json', 'r') as f:
            result = json.load(f)
        self.assertEqual(
            self.varsome_api.lookup('chr19:20082943:1:G'),
            result
            )
        with open(lookup_results + '3.json', 'r') as f:
            result = json.load(f)
        self.assertEqual(
            self.varsome_api.lookup('BRAF:V600E'),
            result
            )
        with open(lookup_results + '4.json', 'r') as f:
            result = json.load(f)
        self.assertEqual(
            self.varsome_api.lookup('TP53:R175L', params='add-source-databases=gerp'),
            result
            )

    def test_batch_lookup(self):
        logging.info('testing batch lookup...')
        batch_result = './test_files/batch_lookup.json'
        variants = [
            'CCR5:c.*1712delG',
            'LIAS:c.*123_*124delAA',
            'SOX4:c.*320_*322delAAA'
            ]

        with open(batch_result, 'r') as f:
            result = json.load(f)
        self.assertEqual(
            self.varsome_api.batch_lookup(variants),
            result
            )

    def tearDown(self):
        self.varsome_api.session.close()
        self.varsome_api_no_auth.session.close()


class Test_CLI(unittest.TestCase):

    def setUp(self):
        self.parser = create_parser()

    def test_parser_no_args(self):
        logging.info('testing parser without args...')
        with self.assertRaises(SystemExit):
            self.parser.parse_args()

    def test_parser_bad_auth(self):
        logging.info('testing parser with bad key file...')
        args = self.parser.parse_args(['-k', 'notafile', '-s', 'null'])
        with self.assertRaises(FileNotFoundError):
            parse_the_args(args)

    def test_parser_single_ref_genome(self):
        logging.info('testing parser with single variant and ref_genome...')
        variant = 'BRAF:V600E'
        ref_genome = 'hg19'

        args = self.parser.parse_args(['-s', variant, '-g', ref_genome,])
        
        self.assertEqual(
            parse_the_args(args),
            (None, variant, ref_genome, None, None)
            )

    def test_parser_authenticated_batch(self):
        logging.info('testing parser with key and batch file...')
        with open('./varsome_api_key', 'r') as f:
            api_key = f.readline().rstrip('\n')

        variants_file = './test_files/batch_sample.txt'
        with open(variants_file, 'r') as f:
            variants = f.readlines()

        args = self.parser.parse_args(
            [
            '-k', './varsome_api_key',
            '-f', variants_file
            ]
            )

        self.assertEqual(
            parse_the_args(args),
            (api_key, None, None, None, variants)
            )

if __name__ == '__main__':
    unittest.main()