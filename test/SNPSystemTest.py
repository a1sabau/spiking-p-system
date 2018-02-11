import unittest

class SNPSystemTest(unittest.TestCase):

    def test_upper2(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
