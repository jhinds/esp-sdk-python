from .sdk import requester, make_endpoint


class ObjectMismatchError(Exception): pass


class ESPResource(object):

    def __init__(self, data):
        if data['type'] != self.plural_name:
            raise ObjectMismatchError('{} cannot store data for {}'.format(
                name, data['type']))
        self.id = data['id']

        for k, v in data['attributes']:
            setattr(self, k, v)

        # relationships are methods and so we store the link to those resources
        # in a property prefixed with an underscore.
        for k, v in data['relationships']:
            setattr(self, '_{}'.format(k), v)

    @property
    def plural_name(self):
        # getting the name like this will break down as soon as we add
        # resources that don't just append an s for pluralization. Fix when
        # that problem arises.
        return self.__class__.__name__.lower() + 's'

    def save(self):
        raise NotImplementedError

    @classmethod
    def get(cls, id):
        pass

    @classmethod
    def all(cls):
        endpoint = make_endpoint(cls.plural_name)
        data = requester(endpoint, 'get')

