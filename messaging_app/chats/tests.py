from django.test import TestCase

class TestSample(TestCase):
    def setUp(self):
        self.x = 4
        
    def test_Calc(self):
        self.assertEqual(self.x, 4)