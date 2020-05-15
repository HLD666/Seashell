import json
import unittest

from flask import g
from node.app import create_app


class StatusUpdateTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # db.create_all()
        self.client = self.app.test_client()
        g.cur_ps = {}
        g.cur_ps.update({1: {"handle": "nothing"}})

    def tearDown(self) -> None:
        # db.drop_all()
        # db.session.remove()
        self.app_context.pop()

    def test_alive_check_response_status(self):
        response = self.client.get('/query_node/',  content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_task_control_response_status(self):
        response = self.client.get('/task/control?task_id=1&operation=stop', content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_alive_check_response_info(self):
        response = self.client.get('/query_node/', content_type='application/json')
        json_response = json.loads(response.get_data(as_text=True))

        self.assertEqual(0, json_response["node_status"])

    def test_task_control_works(self):
        pass
