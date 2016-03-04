from .alert import Alert
from .resource import ESPResource, POST_REQUEST, PaginatedCollection
from .sdk import make_endpoint


class Signature(ESPResource):

    @classmethod
    def create(cls):
        raise NotImplementedError('Alert does not implement a create method')

    def save(self):
        raise NotImplementedError('Alert does not implement a save method')

    def destroy(self):
        raise NotImplementedError('Alert does not implement a destroy method')

    def run(self, external_account_id, region):
        self.external_account_id = external_account_id
        self.region = region
        endpoint = make_endpoint(self._resource_path(self.id_, extra=['run']))
        response = self._make_request(endpoint,
                                      POST_REQUEST,
                                      data=self.to_json())
        data = response.json()
        return PaginatedCollection(Alert, data)
