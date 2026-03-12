import unittest
from model.model import predict

class TestModel(unittest.TestCase):

    def test_predict_basic(self):
        self.assertEqual(predict(0), 1)
        self.assertEqual(predict(10), 11)
        self.assertEqual(predict(-5), -4)

if __name__ == "__main__":
    unittest.main()