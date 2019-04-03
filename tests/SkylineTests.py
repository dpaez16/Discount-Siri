import unittest
from modules.skyline import get_skyline_link


class SkylineTests(unittest.TestCase):
    """
    Runs all tests to make sure that the weather functionality works as expected.
    """

    def test_bad_locations(self):
        """
        Tests to see if the skyline function catches bad locations properly.
        """

        skyline_link = get_skyline_link("asdf", "asdf")
        self.assertEqual(skyline_link, "")

        return

    def test_good_location(self):
        """
        Tests to see if the skyline function catches bad locations properly.
        """

        skyline_link = get_skyline_link("Chicago", "US")
        self.assertNotEqual(skyline_link, "")

        skyline_link = get_skyline_link("Champaign", "US")
        self.assertNotEqual(skyline_link, "")

        skyline_link = get_skyline_link("asdf", "US")
        self.assertEqual(skyline_link, "")

        return


if __name__ == '__main__':
    unittest.main()
