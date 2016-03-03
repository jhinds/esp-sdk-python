from .resource import ESPResource


class CloudTrailEvent(ESPResource):

    @classmethod
    def create(cls):
        raise NotImplementedError('CloudTrailEvent does not implement a create method')

    def save(self):
        raise NotImplementedError('CloudTrailEvent does not implement a save method')

    def destroy(self):
        raise NotImplementedError('CloudTrailEvent does not implement a destroy method')
