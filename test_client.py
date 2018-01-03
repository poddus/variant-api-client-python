import unittest
from variantapi.client import VariantAPIClient
from variantapi.client import VarsomeHTTPError

# produces a lot of ResourceWarnings from Requests
# production code runs fine, so we can ignore

class TestAPIOutput(unittest.TestCase):

    def setUp(self):
        self.variants = [
            'CCR5:c.*1712delG',
            'LIAS:c.*123_*124delAA',
            'SOX4:c.*320_*322delAAA'
            ]

    def test_HTTP_error_handling(self):
        # don't pass API key to raise 401 Error
        self.varsome_api = VariantAPIClient()
        with self.assertRaises(VarsomeHTTPError):
            self.varsome_api.batch_lookup(self.variants)

    def test_lookup(self):
        self.varsome_api = VariantAPIClient()
        self.assertEqual(
            self.varsome_api.lookup(self.variants[0]),
            {
             'chromosome': 'chr3',
             'alt': '',
             'ref': 'G',
             'pos': 46417157,
             'variant_id': '10190030464171579001',
             'variant_type': 'Deletion (homopolymer)',
             'cytobands': '3p21.31'
            }
            )
        self.varsome_api.lookup(self.variants[0])

    def test_batch_lookup(self):
        with open('../varsome_api_key', 'r') as f:
            self.key = f.read()

        self.varsome_api = VariantAPIClient(self.key)
        self.assertEqual(
            self.varsome_api.batch_lookup(self.variants),
            [{'alt': '',
              'chromosome': 'chr3',
              'cytobands': '3p21.31',
              'pos': 46417157,
              'ref': 'G',
              'variant_id': '10190030464171579001',
              'variant_type': 'Deletion (homopolymer)'},
             [{'alt': '',
               'chromosome': 'chr4',
               'cytobands': '4p14',
               'pos': 39478849,
               'ref': 'AA',
               'variant_id': '10190040394788499002',
               'variant_type': 'Deletion (homopolymer)'},
              {'alt': '',
               'chromosome': 'chr4',
               'cytobands': '4p14',
               'pos': 39465352,
               'ref': 'AA',
               'variant_id': '10190040394653528001',
               'variant_type': 'Deletion (homopolymer)'}],
             {'alt': '',
              'chromosome': 'chr6',
              'cytobands': '6p22.3',
              'pos': 21596502,
              'ref': 'AAA',
              'variant_id': '10190060215965029003',
              'variant_type': 'Deletion (homopolymer)'}]
            )

if __name__ == '__main__':
    unittest.main()