import unittest
from unittest.mock import patch
from io import StringIO
import sys


import graph

BASE_URL = 'http://sam-user-activity.eu-west-1.elasticbeanstalk.com/'

data={
    "01-01-2022":300,"02-01-2022":500,"03-01-2022":700,"04-01-2022":1300,
    "05-01-2022":2000,"06-01-2022":3000,"07-01-2022":3500,
    }

class TestGraphLogic(unittest.TestCase):
    instance = graph.Graph(BASE_URL)

    def test_is_integer_pass(self):
        answer = StringIO()
        sys.stdout = answer
        output = self.instance.is_integer(2)
        self.assertTrue(output)
        
    def test_is_integer_fail(self):
        answer = StringIO()
        sys.stdout = answer
        output = self.instance.is_integer('2')
        self.assertFalse(output)

    def test_is_date_invalid(self):
        answer = StringIO()
        sys.stdout = answer
        output = self.instance.is_date(list(data.keys()),'01-02-2026')
        self.assertFalse(output)
        
    def test_is_date_valid(self):
        answer = StringIO()
        sys.stdout = answer
        output = self.instance.is_date(list(data.keys()),'01-01-2022')
        self.assertTrue(output)           
        
    def test_is_valid_date_true(self):
        answer = StringIO()
        sys.stdout = answer
        output = self.instance.validate_date('01-01-2022')
        self.assertTrue(output)   

    
if __name__ == '__main__':
    unittest.main()