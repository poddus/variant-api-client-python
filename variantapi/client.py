import logging
import requests

__author__ = 'saphetor, Leopold von Seckendorff'

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO
    )

class VarsomeHTTPError(Exception):
    ERROR_CODES = {
        400: "Bad request. A parameter you have passed is not valid, "
             "or something in your request is wrong",
        401: "Not Authorized: either you need to provide authentication "
             "credentials, or the credentials provided aren't valid.",
        403: "Bad Request: your request is invalid, and we'll return "
             "an error message that tells you why. This is the "
             "status code returned if you've "
             "exceeded the rate limit (see below).",
        404: "Not Found: either you're requesting an invalid URI "
             "or the resource in question doesn't exist",
        500: "Internal Server Error: we did something wrong.",
        501: "Not implemented.",
        502: "Bad Gateway: returned if VariantAPI is down or being upgraded.",
        503: "Service Unavailable: the VariantAPI servers are up, "
             "but are overloaded with requests. Try again later.",
        504: "Gateway Timeout",
    }

    def __init__(self, status):
        super().__init__('{} ({})'.format(status, self.ERROR_CODES[status]))

class VariantAPIClientBase(object):
    _api_url = 'https://api.varsome.com'

    def __init__(self, api_key=None):
        self._headers = {'Accept': 'application/json'}

        if api_key is not None:
            self._headers['Authorization'] = 'Token ' + api_key

        self.session = requests.Session()
        self.session.headers.update(self._headers)

    def _make_request(self, path, method='GET', params=None, json_data=None):
        logging.debug('get request to ' + self._api_url + path)
        if method == 'GET':
            r = self.session.get(self._api_url + path, params=params)
        elif method == 'POST':
            r = self.session.post(
                self._api_url + path,
                params=params,
                json=json_data,
                headers={'Content-Type': 'application/json'}
                    if json_data is not None else None
                )
            logging.debug(
                'response time {}'.format(r.elapsed)
                )
            logging.debug('Content length {}'.format(len(r.content)))

        if r.status_code in VarsomeHTTPError.ERROR_CODES:
            raise VarsomeHTTPError(r.status_code)

        return r

    def get(self, path, params=None):
        response = self._make_request(path, 'GET', params=params)
        return response.json()

    def post(self, path, params=None, json_data=None):
        response = self._make_request(
                        path,
                        'POST',
                        params=params,
                        json_data=json_data
                        )
        return response.json()


class VariantAPIClient(VariantAPIClientBase):
    schema_lookup_path = '/lookup/schema'
    lookup_path = '/lookup/'
    batch_lookup_path = '/lookup/batch/'

    def __init__(self, api_key=None, batch_size=10000):
        super(VariantAPIClient, self).__init__(api_key)
        self.batch_size = batch_size

    def schema(self):
        return self.get(self.schema_lookup_path)

    def lookup(self, query, params=None, ref_genome=None):
        """

        :param query: variant representation
        :param params: dictionary of key value pairs for
            http GET parameters. Refer to the api documentation
        of https://api.varsome.com for examples
        :param ref_genome: reference genome (hg19 or hg38)
        :return:dictionary of annotations. refer to
            https://api.varsome.com/lookup/schema for dictionary properties
        """
        if ref_genome is not None:
            full_path = self.lookup_path + query + '/' + ref_genome
        else:
            full_path = self.lookup_path + query

        return self.get(full_path, params=params)

    def batch_lookup(self, variants, params=None, ref_genome=None):
        """return list of query results for all variants.

        split variants into chunks of size batch_size.
        post GET for each chunk, but return combined results.

        :param variants: list of variant representations
        :param params: dictionary of key value pairs for http GET parameters.
            Refer to the api documentation of
            https://api.varsome.com for examples
        :param ref_genome: reference genome (hg19 or hg38)
        :return: list of dictionaries with annotations per variant
            refer to https://api.varsome.com/lookup/schema
            for dictionary properties
        """
        if ref_genome is not None:
            full_path = self.batch_lookup_path + ref_genome
        else:
            full_path = self.batch_lookup_path + 'hg19'

        n = self.batch_size
        chunks = [variants[i:i+n] for i in range(0, len(variants), n)]

        results = []
        for chunk in chunks:
            data = self.post(
                        full_path,
                        params=params,
                        json_data={'variants': chunk}
                        )
            results.extend(data)
        return results
