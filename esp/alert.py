from .resource import ESPResource


class Alert(ESPResource):

    @classmethod
    def create(cls):
        raise NotImplementedError('Alert does not implement a create method')

    def save(self):
        raise NotImplementedError('Alert does not implement a save method')

    def destroy(self):
        raise NotImplementedError('Alert does not implement a destroy method')
