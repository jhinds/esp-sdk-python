import json
import mock
import unittest

import esp


class TestResource(unittest.TestCase):

    def setUp(self):
        self.report1 = {
            'id': '1',
            'type': 'reports',
            'attributes': {
                'status': 'completed',
                'created_at': '2016-02-26T18:00:00.000Z',
                'updated_at': '2016-02-26T18:03:48.000Z',
            },
            'relationships': {
                'alerts': {
                    'links': {
                        'related': 'http://localhost:3000/api/v2/reports/1/alerts.json'
                    }
                },
                'organization': {
                    'links': {
                        'related': 'http://localhost:3000/api/v2/reports/1/organization.json'
                    }
                },
                'sub_organization': {
                    'links': {
                        'related': 'http://localhost:3000/api/v2/reports/1/sub_organization.json'
                    }
                },
                'team': {
                    'links': {
                        'related': 'http://localhost:3000/api/v2/reports/1/team.json'
                    }
                },
            }
        }

        self.report2 = {
            'id': '2',
            'type': 'reports',
            'attributes': {
                'status': 'processing',
                'created_at': '2016-02-26T18:00:00.000Z',
                'updated_at': '2016-02-26T18:03:48.000Z',
            },
            'relationships': {
                'alerts': {
                    'links': {
                        'related': 'http://localhost:3000/api/v2/reports/2/alerts.json'
                    }
                },
                'organization': {
                    'links': {
                        'related': 'http://localhost:3000/api/v2/reports/2/organization.json'
                    }
                },
                'sub_organization': {
                    'links': {
                        'related': 'http://localhost:3000/api/v2/reports/2/sub_organization.json'
                    }
                },
                'team': {
                    'links': {
                        'related': 'http://localhost:3000/api/v2/reports/2/team.json'
                    }
                },
            }
        }

        self.report_response = json.dumps({'data': self.report1})
        self.reports_response = json.dumps({'data': [self.report1, self.report2]})

        esp.settings.settings.access_key_id = 'abc'
        esp.settings.settings.secret_access_key = 'abc123'
        esp.settings.settings.host = 'http://localhost:3000'

    @mock.patch('esp.sdk.requests.get')
    def test_can_fetch_a_single_resource(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = json.loads(self.report_response)
        mock_get.return_value = mock_response

        report = esp.Report.find(id=1)

        self.assertIsInstance(report, esp.report.Report)
        self.assertEqual(report.status, 'completed')
        self.assertEqual(report.id, '1')

    @mock.patch('esp.sdk.requests.get')
    def test_relationships_are_cachedrelationships(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = json.loads(self.report_response)
        mock_get.return_value = mock_response

        report = esp.Report.find(id=1)

        self.assertIsInstance(report._attributes['alerts'], esp.resource.CachedRelationship)
        self.assertIsInstance(report._attributes['organization'], esp.resource.CachedRelationship)
        self.assertIsInstance(report._attributes['sub_organization'], esp.resource.CachedRelationship)
        self.assertIsInstance(report._attributes['team'], esp.resource.CachedRelationship)

    @mock.patch('esp.sdk.requests.get')
    def test_can_fetch_a_collection(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = json.loads(self.reports_response)
        mock_get.return_value = mock_response
        reports = esp.Report.find()

        self.assertIsInstance(reports, esp.resource.PaginatedCollection)
        self.assertEqual(len(reports), 2)
