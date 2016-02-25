import importlib

from .sdk import requester, make_endpoint
from .packages import six
from .utilities import (pluralize,
                        singularize,
                        titlecase_to_underscore,
                        underscore_to_titlecase)

GET_REQUEST = 'get'
POST_REQUEST = 'post'
PUT_REQUEST = 'put'
DELETE_REQUEST = 'delete'


class ObjectMismatchError(Exception):
    pass


class RelationshipDoesNotExist(Exception):
    pass


class PaginatedCollection(object):
    pass


def find_class(name):
    package = '.'.join(__name__.split('.')[:-1])
    module = importlib.import_module('.{}'.format(name), package=package)
    return getattr(module, underscore_to_titlecase(name))


class CachedRelationship(object):

    def __init__(self, name, rel):
        self.name = name
        self.endpoint = rel['links']['related']
        self._cached_collection = None

    def fetch(self):
        if not self._cached_collection:
            response = requester(self.endpoint, GET_REQUEST)
            if response.status_code != 200:
                response.raise_for_status()
            data = response.json()['data']
            # TODO(kt) detect pagination responses and create a paginated
            # collection
            cls = find_class(self.name)
            self._cached_collection = [cls(resource) for resource in data]
        return self._cached_collection

    def reload(self):
        self._cached_collection = None


class ESPMeta(type):

    def __new__(cls, name, bases, dct):
        dct['resource_name'] = pluralize(titlecase_to_underscore(name))
        return super(ESPMeta, cls).__new__(cls, name, bases, dct)


class ESPResource(six.with_metaclass(ESPMeta, object)):

    def __init__(self, data):
        if data['type'] != self.resource_name:
            raise ObjectMismatchError('{} cannot store data for {}'.format(
                self.resource_name, data['type']))

        self._attributes = {}
        self._attributes['type'] = data['type']
        self._attributes['id'] = data['id']

        for k, v in data['attributes'].items():
            self._attributes[k] = v

        for k, v in data['relationships'].items():
            self._attributes[k] = CachedRelationship(singularize(k), v)
        self.init_complete = True

    def __getattr__(self, attr):
        if '_attributes' in self.__dict__:
            if attr in self._attributes:
                val = self._attributes[attr]
                if isinstance(val, CachedRelationship):
                    return val.fetch()
                return val
        raise AttributeError(attr)

    def __setattr__(self, attr, value):
        if 'init_complete' in self.__dict__:
            if attr in self.__dict__ or getattr(self.__class__, attr, None):
                object.__setattr__(self, attr, value)
            else:
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
        return '{name}'.format(name=pluralize(cls.__name__))

    @classmethod
    def find(cls, id=None):
        if not id:
            return cls._all()
        return cls._get(id)

    @classmethod
    def _get(cls, id):
        endpoint = make_endpoint(cls._resource_path(id))
        response = cls._make_request(endpoint, GET_REQUEST)
        if response.status_code == 200:
            data = response.json()
            return data['data']
        return None

    @classmethod
    def _all(cls):
        endpoint = make_endpoint(cls._resource_collection_path())
        response = cls._make_request(endpoint, GET_REQUEST)
        if response.status_code == 200:
            data = response.json()
            for record in data['data']:
                yield cls(record)
        yield

    @classmethod
    def create(**kwargs):
        pass

    def to_json(self):
        """
        This is the method that will convert class data to a json string
        """

    def save(self):
        raise NotImplementedError
