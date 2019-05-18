from __future__ import unicode_literals

import datetime

try:
    from urllib.parse import urljoin
except ImportError:  # For Python 2
    from urlparse import urljoin  # noqa

import requests

from .exceptions import FixerioException

BASE_URL = 'http://data.fixer.io/'
SECURE_BASE_URL = 'https://data.fixer.io/'

LATEST_PATH = '/latest'

DEFAULT_BASE = 'EUR'  # Rates are quoted against the Euro by default.


class Fixerio(object):
    """ A client for Fixer.io. """

    def __init__(self, base=DEFAULT_BASE, access_key=None, symbols=None, secure=False):
        """
        :param base: currency to quote rates.
        :type base: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :param secure: enable HTTPS endpoint.
        :type secure: bool
        """
        self.base = base if base != DEFAULT_BASE else None
        self.symbols = symbols
        self.secure = secure
        self.access_key = access_key # change Alex

        if self.access_key is None:
           raise FixerioException('You need to provide an access key!')

    @staticmethod
    def _create_payload(base, symbols):
        """ Creates a payload with no none values.

        :param base: currency to quote rates.
        :type base: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: a payload.
        :rtype: dict
        """
        payload = {}
        if base is not None:
            payload['base'] = base
        if symbols is not None:
            payload['symbols'] = ','.join(symbols)

        return payload

    @staticmethod
    def _secure_url(secure, path):
        """
        Builds a URL. If `secure` is `True`, HTTPS endpoint is used. Otherwise
        HTTP endpoint.

        :param secure: enable HTTPS endpoint.
        :type secure: bool
        :param path: URL path component
        :type path: unicode
        :return: a URL
        """
        if secure:
            url = urljoin(SECURE_BASE_URL, path)
        else:
            url = urljoin(BASE_URL, path)

        return url

    def latest(self, base=None, symbols=None, secure=False):
        """ Get the latest foreign exchange reference rates.

        :param base: currency to quote rates.
        :type base: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :param secure: enable HTTPS endpoint.
        :type secure: bool
        :return: the latest foreign exchange reference rates.
        :rtype: dict
        :raises FixerioException: if any error making a request.
        """
        try:
            base = base or self.base
            symbols = symbols or self.symbols
            payload = Fixerio._create_payload(base, symbols)

            # latest path with access key
            LATEST_PATH_WITH_KEY = urljoin(LATEST_PATH,'?access_key='+self.access_key)

            secure = secure or self.secure
            url = Fixerio._secure_url(secure, LATEST_PATH_WITH_KEY)

            response = requests.get(url, params=payload) # ALEX change

            response.raise_for_status() # ALEX change
            #return url # ALEX change

            return response.json() # ALEX change
        except requests.exceptions.RequestException as ex:
            raise FixerioException(str(ex))

    def historical_rates(self, date, base=None, symbols=None, secure=False):
        """
        Get historical rates for any day since `date`.

        :param date: a date
        :type date: date or str
        :param base: currency to quote rates.
        :type base: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :param secure: enable HTTPS endpoint.
        :type secure: bool
        :return: the historical rates for any day since `date`.
        :rtype: dict
        :raises FixerioException: if any error making a request.
        """
        try:
            if isinstance(date, datetime.date):
                # Convert date to ISO 8601 format.
                date = date.isoformat()

            # add the access key # change Alex
            date_with_key = date + '?access_key='+self.access_key # change Alex

            base = base or self.base
            symbols = symbols or self.symbols
            payload = Fixerio._create_payload(base, symbols)

            secure = secure or self.secure
            url = Fixerio._secure_url(secure, date_with_key) # change Alex

            response = requests.get(url, params=payload)

            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as ex:
            raise FixerioException(str(ex))
