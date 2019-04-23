import unittest
from modules.spongebob_mock import gen_spongebob_mock


class SpongemockTests(unittest.TestCase):
    """
    Runs all tests to make sure that the "spongemock" functionality works as expected.
    """

    def test_proper_output(self):
        """
        Tests to see if the "spongemock" functionality works as expected.
        """

        text_input = ""
        self.assertEqual(gen_spongebob_mock(text_input), "")

        text_input = "241 sucks"
        self.assertEqual(gen_spongebob_mock(text_input), "241 sUcKs")

        text_input = "the fitness gram pacer test"
        self.assertEqual(gen_spongebob_mock(text_input), "tHe fItNeSs gRaM PaCeR TeSt")

        text_input = "\n  \n 241 sucks\n\t\n    "
        self.assertEqual(gen_spongebob_mock(text_input), "241 sUcKs")

        return


if __name__ == '__main__':
    unittest.main()
