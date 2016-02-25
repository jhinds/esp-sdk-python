from .sdk import requester, make_endpoint
from .utilities import pluralize
from .packages import six

GET_REQUEST = 'get'
POST_REQUEST = 'post'
PUT_REQUEST = 'put'
DELETE_REQUEST = 'delete'


class ObjectMismatchError(Exception):
    pass


class RelationshipDoesNotExist(Exception):
    pass


class ESPMeta(type):

    def __new__(cls, name, bases, dct):
        dct['class_name'] = name.lower()
        return super(ESPMeta, cls).__new__(cls, name, bases, dct)


class ESPResource(six.with_metaclass(ESPMeta, object)):

    def __init__(self, data):
        if data['type'] != self.plural_name:
            raise ObjectMismatchError('{} cannot store data for {}'.format(
                self.plural_name, data['type']))

        self._attributes = {}
        self._attributes['type'] = data['type']
        self._attributes['id'] = data['id']

        for k, v in data['attributes'].items():
            self._attributes[k] = v

        # relationships are methods and so we store the link to those resources
        # in a property prefixed with an underscore.
        for k, v in data['relationships'].items():
            self._attributes[k] = v

    def __getattr__(self, attr):
        if attr in self._attributes:
            return self._attributes[attr]
        raise AttributeError(attr)

    def __setattr__(self, attr, value):
        if attr in self._attributes:
            self._attributes[attr] = value
        else:
            object.__setattr__(self, attr, value)

    @classmethod
    def _make_request(cls, endpoint, request_type):
        return requester(endpoint, request_type)

    @classmethod
    def _resource_path(cls, id):
        return '{name}/{id}'.format(name=pluralize(cls.__name__), id=id)

    @classmethod
    def _resource_collection_path(cls):
        return '{name}'.format(pluralize(cls.__name__))

    def find(cls, id=None):
        if not id:
            return cls._all()
        return cls._get(id)

    @classmethod
    def _get(cls, id):
        endpoint = make_endpoint(cls._resource_path(id))
        response = cls.requester(endpoint, 'get')
        if response.status_code == 200:
            data = response.json()
            return data['data']
        return None

    @classmethod
    def _all(cls):
        endpoint = make_endpoint(cls._resource_collection_path())
        response = cls.requester(endpoint, 'get')
        if response.status_code == 200:
            data = response.json()
            for record in data['data']:
                yield cls(record)
        yield

    def _relationship_endpoint(self, rel_name):
        if not hasattr(self, rel_name):
            raise RelationshipDoesNotExist
        rel = getattr(self, rel_name)
        return rel['links']['related']

    def to_json(self):
        """
        This is the method that will convert class data to a json string
        """

    def save(self):
        raise NotImplementedError
