# coding: utf-8
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import logging

import requests

from .auth import ESPAuth
from .settings import settings

logger = logging.getLogger(__name__)


def make_endpoint(uri):
    url = '{}{}/{}'.format(settings.host, settings.api_prefix, uri)
    return url


def requester(url, request_type, headers={}, data=None):
    logging.debug('Making request to {}'.format(url))
    headers['User-Agent'] = settings.user_agent
    method = getattr(requests, request_type)
    response = method(url, data=data, headers=headers, auth=ESPAuth(
        access_key_id=settings.access_key_id,
        secret_access_key=settings.secret_access_key
    ))
    return response.json()


#class ESP(object):
#
#    registry = {}
#    endpoints = {}
#
#    def __init__(self,
#                 base_url=DEFAULT_BASE_URL,
#                 access_key_id=None,
#                 secret_access_key=None,
#                 user_agent=DEFAULT_USER_AGENT):
#        """
#        :param base_url: string
#        :param access_key_id: string
#        :param secret_access_key: string
#        """
#        self.access_key_id = access_key_id or getattr(
#            os.environ['ESP_ACCESS_KEY_ID'], None)
#        self.secret_access_key = secret_access_key or getattr(
#            os.environ['ESP_SECRET_ACCESS_KEY'], None)
#        if not self.access_key_id or not self.secret_access_key:
#            raise KeyError('access_key_id and secret_access_key are required')
#        self.base_url = base_url
#        self.user_agent = DEFAULT_USER_AGENT
#
#    def register_endpoint(self, name, uri):
#        def wrapper(f):
#            self.registry[name] = {'callback': f, 'uri': uri}
#            return f
#        return wrapper
#
#
#
#
#    def alerts(self):
#        logger.debug('Fetching alerts')
#        url = _make_endpoint('/alerts')
#        data = self._make_http_request(url, 'get')
#        alerts = []
#        for obj in data['data']:
#            alerts.append(Alert(obj))
#
#        return alerts
#
#
#def new_esp_sdk(raise_exception_on_failure=True):
#    token, email = fetch_token()
#    wrapped = functools.partial(call_api,
#                                email=email,
#                                token=token,
#                                raise_exception_on_failure=raise_exception_on_failure)
#    return wrapped
#
#
#def call_api(endpoint, email=None, token=None,
#             raise_exception_on_failure=True, **kwargs):
#    try:
#        endpoint_dict = registry[endpoint]
#    except:
#        raise LookupError('Could not find endpoint: {}'.format(endpoint))
#    headers = {'Authorization-Email': email,
#               'Authorization': token,
#               'Content-Type': 'application/json',
#               'Accept': 'application/json',
#               'User-Agent': 'Pythia {}'.format(get_version())}
#    func = endpoint_dict['callback']
#    try:
#        resp = func(endpoint_dict['uri'], headers, **kwargs)
#        return resp
#    except Exception as e:
#        if raise_exception_on_failure:
#            raise e
#
#
#
#
#
#
#@register_endpoint('external_accounts', 'external_accounts')
#def external_accounts_request(uri, headers):
#    accounts = []
#    page = 1
#    done = False
#    while not done:
#        endpoint = make_endpoint(uri)
#        url = endpoint + '?page={}'.format(page)
#        response = make_http_request(url, 'get', headers)
#        if response.status_code == 200:
#            account_data = response.json()
#            if len(account_data) > 0:
#                for a in account_data:
#                    accounts.append({
#                        'account': a['account'],
#                        'arn': a['arn'],
#                        'organization_id': a['organization_id'],
#                        'external_id': a['external_id']})
#                page += 1
#            else:
#                done = True
#        else:
#            response.raise_for_status()
#    return accounts
#
#
#@register_endpoint('external_account', 'external_accounts/{}')
#def external_account_request(uri, headers, account_id):
#    endpoint = make_endpoint(uri)
#    url = endpoint.format(account_id)
#    response = make_http_request(url, 'get', headers)
#    account = None
#    if response.status_code == 200:
#        account = response.json()
#    else:
#        response.raise_for_status()
#    return account
#
#
#@register_endpoint('alerts', 'reports/{}/alerts')
#def alerts_request(uri, headers, report_id):
#    alerts = []
#    page = 1
#    done = False
#    while not done:
#        endpoint = make_endpoint(uri)
#        url = endpoint.format(report_id) + '?page={}'.format(page)
#        response = make_http_request(url, 'get', headers)
#        if response.status_code == 200:
#            alert_data = response.json()
#            if len(alert_data) > 0:
#                alerts.extend(alert_data)
#                page += 1
#            else:
#                done = True
#        else:
#            response.raise_for_status()
#    return alerts
#
#
#@register_endpoint('alert', 'alerts/{}')
#def alert_request(uri, headers, alert_id):
#    endpoint = make_endpoint(uri)
#    url = endpoint.format(alert_id)
#    response = make_http_request(url, 'get', headers)
#    if response.status_code != 200:
#        response.raise_for_status()
#    return response.json()
