import base64
from datetime import datetime
import hashlib
import hmac
from time import mktime
from urllib.parse import urlparse
from wsgiref.handlers import format_date_time
from requests.auth import AuthBase

CONTENT_TYPE = 'application/vnd.api+json'


class UnauthorizedError(Exception):
    pass


class ESPAuth(AuthBase):
    """
    An instance of this class should be passed into a requests call as
    the `auth` parameter.
    """

    def __call__(self, r):
        """
        :param r: requests Request object instance
        :type r: requests.Request
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
        :param access_key_id: public access key from ESP
        :type access_key_id: string
        :param secret_access_key: secret access key from ESP
        :type secret_access_key: string
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
        return b64.decode()

    def sign_request(self, r):
        """
        :param r: requests Request object instance
        :type r: requests.Request
        :returns: str

        Sign request takes pieces of information about the request and
        generates a hmac hash digest for authentication. This will return a
        base64 string of the digest
        """
        url = urlparse(r.url)
        canonical = '{content_type},{md5},{uri},{date}'.format(
            content_type=CONTENT_TYPE,
            md5=self.body_md5(r.body),
            uri=url.path,
            date=self.date)
        digest = hmac.new(self.secret_access_key.encode('utf-8'),
                     canonical.encode('utf-8'),
                     digestmod=hashlib.sha1).digest()
        return 'APIAuth {access_key}:{signature}'.format(
            access_key=self.access_key_id,
            signature=base64.b64encode(digest).decode())
