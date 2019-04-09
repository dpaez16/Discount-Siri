import unittest
from modules.random_shower_thought import get_random_shower_thought


class RandomFactTests(unittest.TestCase):
    """
    Runs all tests to make sure that the random shower thought function works as expected.
    """

    def test_proper_format(self):
        """
        Tests to see if the random shower thought function works as expected.
        """

        random_shower_thought = get_random_shower_thought()
        self.assertTrue(random_shower_thought)

        return


if __name__ == '__main__':
    unittest.main()
