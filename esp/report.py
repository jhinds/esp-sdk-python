from .resource import ESPResource


class Report(ESPResource):

    def save(self):
        raise NotImplementedError('Report does not implement a save method')

    def destroy(self):
        raise NotImplementedError('Report does not implement a destroy method')
