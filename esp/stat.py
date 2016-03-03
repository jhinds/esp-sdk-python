from .resource import ESPResource


class Stat(ESPResource):

    @classmethod
    def list(cls):
        raise NotImplementedError('Stat does not implement a list method')

    @classmethod
    def create(cls):
        raise NotImplementedError('Stat does not implement a create method')

    def save(self):
        raise NotImplementedError('Stat does not implement a save method')

    def destroy(self):
        raise NotImplementedError('Stat does not implement a destroy method')
