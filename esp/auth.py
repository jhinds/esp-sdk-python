import base64
from datetime import datetime
import hashlib
import hmac
from time import mktime
from urllib.parse import urlparse
from wsgiref.handlers import format_date_time

CONTENT_TYPE = 'application/vnd.api+json'


class ESPAuth(object):

    def __call__(self, r):
        """
        :param r: requests.Request
        """
        now = datetime.now()
        tt = mktime(now.timetuple())
        self.date = format_date_time(tt)
        r.headers['Authorization'] = self.sign_request(r)
        r.headers['Content-MD5'] = self.body_md5(r.body)
        r.headers['Content-Type'] = CONTENT_TYPE
        r.headers['Accept'] = CONTENT_TYPE
        r.headers['Date'] = self.date
        return r

    def __init__(self, access_key_id, secret_access_key):
        """
        :param access_key_id: string
        :param secret_access_key: string
        """
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.date = None # set at the time of __call__ in case of reuse

    def body_md5(self, body=None):
        """
        :type: string

        Returns a base64 string of the content body passed in.
        """
        if not body:
            body = ''
        body_bytes = body.encode('utf-8')
        b64 = base64.b64encode(hashlib.md5(body_bytes).digest())
        return b64

    def sign_request(self, r):
        """
        :type: string
        """
        url = urlparse(r.url)
        cannonical = '{content_type},{md5},{uri},{date}'.format(
            content_type=CONTENT_TYPE,
            md5=self.body_md5(r.body),
            uri=url.path,
            date=self.date)
        h = hmac.new(self.secret_access_key.encode('utf-8'),
                     cannonical.encode('utf-8'),
                     hashlib.sha1)
        return 'APIAuth {access_key}:{signature}'.format(
            access_key=self.access_key_id,
            signature=base64.b64encode(h.digest()).strip())
