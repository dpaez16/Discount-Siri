import unittest
from modules.random_fact import get_random_fact


class RandomFactTests(unittest.TestCase):
    """
    Runs all tests to make sure that the random fact function works as expected.
    """

    def test_proper_format(self):
        """
        Tests to see if the random fact function works as expected.
        """

        random_fact = get_random_fact()
        self.assertTrue(random_fact)

        return


if __name__ == '__main__':
    unittest.main()
