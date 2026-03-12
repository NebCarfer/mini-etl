import unittest
from batch.clean import clean
from batch.transform import transform
from batch.send import send
import os
import json

class TestBatchPipeline(unittest.TestCase):

    def test_clean_valid(self):
        records = [{"value": "5"}, {"value": "10"}]
        cleaned = clean(records)
        self.assertEqual(cleaned, [5, 10])

    def test_clean_invalid(self):
        records = [{"value": "a"}, {"value": "10"}]
        cleaned = clean(records)
        self.assertEqual(cleaned, [10])

if __name__ == "__main__":
    unittest.main()