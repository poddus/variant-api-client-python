#!/usr/bin/env python3

import unittest
import logging
import json

from variantapi.client import VariantAPIClient
from variantapi.client import VarsomeHTTPError

from run import create_parser

__author__ = 'Leopold von Seckendorff'

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
    )

class TestClient(unittest.TestCase):

    def setUp(self):
        with open('./varsome_api_key', 'r') as f:
            self.key = f.read()

        self.varsome_api_no_auth = VariantAPIClient()
        self.varsome_api = VariantAPIClient(self.key)

    def test_HTTP_error_handling(self):
        logging.info('testing HTTP Error Handling...')
        # don't pass API key to raise 401 Error
        with self.assertRaises(VarsomeHTTPError):
            self.varsome_api_no_auth.batch_lookup(['BRAF:V600E'])

    def test_schema(self):
        logging.info('testing lookup schema...')
        with open('./test_results/schema.json', 'r') as f:
            results = json.loads(f.read())
        self.assertEqual(
            self.varsome_api.schema(),
            results
            )

    def test_lookup(self):
        logging.info('testing lookups...')
        lookup_results = './test_results/lookup/'

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
        batch_result = './test_results/batch_lookup.json'
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
        with self.assertRaises(SystemExit):
            self.parser.parse_args()

    def test_parser_with_query(self):
        raise NotImplementedError

    def test_parser_with_file(self):
        raise NotImplementedError
         

if __name__ == '__main__':
    unittest.main()