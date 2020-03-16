
import unittest # The test framework
import code.inc_dec as handler # The code to be tested

class Test_TestIncrementDecrement(unittest.TestCase):

    # The first function
    def test_increment(self):
        self.assertEqual(handler.increment(3),4)
    
    # The second function
    def test_decrement(self):
        self.assertEqual(handler.decrement(3),2)

if __name__ == "__main__":
    unittest.main()