import unittest
import csv

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from unittest.mock import patch

from main import init
from utils import validate_url

class ShorteningTestCase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        return init()


    @unittest_run_loop
    async def test_short(self):
        resp = await self.client.request("POST", "/short/", json={'url': 'https://stackoverflow.com/question/'})
        assert resp.status == 200
        text = await resp.text()
        assert "url" in text
    
    @unittest_run_loop
    async def test_short_bad(self):
        resp = await self.client.request("POST", "/short/", json={'sa': 'https://stackoverflow.com/question/'})
        assert resp.status == 400
        text = await resp.text()
        assert "url not in body" in text

class TestValidation(unittest.TestCase):
    """Tests util function
    """
    def setUp(self):
        self.func = validate_url

    def test_function(self):
        """Tests url validation 
        """
        with open('./test_info.csv', 'r') as mock_urls:
            reader = csv.reader(mock_urls, delimiter=',')
            for row in reader:
                valid = self.func(row[0])
                self.assertEqual(valid, bool(int(row[1])))


if __name__ == '__main__':
    unittest.main()