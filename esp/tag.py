from .resource import ESPResource


class Tag(ESPResource):

    @classmethod
    def create(cls):
        raise NotImplementedError('Tag does not implement a create method')

    def save(self):
        raise NotImplementedError('Tag does not implement a save method')

    def destroy(self):
        raise NotImplementedError('Tag does not implement a destroy method')
