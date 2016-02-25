from .resource import ESPResource, GET_REQUEST


class Report(ESPResource):

    @property
    def alerts(self):
        """
        This property method looks up the link from the _alerts dict
        """
        response = self._make_request(self._relationship_endpoint('_alerts'),
                                      GET_REQUEST)
