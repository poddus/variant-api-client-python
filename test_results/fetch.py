import json
from variantapi.client import VariantAPIClient

with open('./varsome_api_key', 'r') as f:
    key = f.read()

varsome_api = VariantAPIClient(key)

### schema
with open('./test_results/schema.json', 'w+') as f:
    json.dump(varsome_api.schema())

### lookup
lookup_results = './test_results/lookup/'
with open(lookup_results + '0.json', 'w+') as f:
    json.dump(varsome_api.lookup('10190091015942290001'), f)

with open(lookup_results + '1.json', 'w+') as f:
    json.dump(varsome_api.lookup('rs113488022', ref_genome='hg38'), f)

with open(lookup_results + '2.json', 'w+') as f:
    json.dump(varsome_api.lookup('chr19:20082943:1:G'), f)

with open(lookup_results + '3.json', 'w+') as f:
    json.dump(varsome_api.lookup('BRAF:V600E'), f)

with open(lookup_results + '4.json', 'w+') as f:
    json.dump(varsome_api.lookup('TP53:R175L', params='add-source-databases=gerp'), f)

### batch_lookup
with open('./test_results/batch_lookup.json', 'w+') as f:
    variants = [
        'CCR5:c.*1712delG',
        'LIAS:c.*123_*124delAA',
        'SOX4:c.*320_*322delAAA'
        ]
    json.dump(varsome_api.batch_lookup(variants), f)
