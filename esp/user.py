from .resource import ESPResource


class User(ESPResource):

    @classmethod
    def create(cls):
        raise NotImplementedError('User does not implement a create method')

    def save(self):
        raise NotImplementedError('User does not implement a save method')

    def destroy(self):
        raise NotImplementedError('User does not implement a destroy method')
