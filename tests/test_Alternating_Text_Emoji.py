import unittest
from modules.alternating_emoji import gen_alternating_emoji


class AlternatingTextEmojiTests(unittest.TestCase):
    """
    Runs all tests to make sure that the "alternating text/emoji" functionality works as expected.
    """

    def test_proper_output(self):
        """
        Tests to see if the "alterning text/emoji" functionality works as expected.
        """

        text_input = ""
        self.assertEqual(gen_alternating_emoji(text_input), "")

        text_input = "241 sucks"
        self.assertEqual(gen_alternating_emoji(text_input), "\U0001F44F 241 \U0001F44F sucks")

        text_input = "the fitness gram"
        self.assertEqual(gen_alternating_emoji(text_input),
                         "\U0001F44F the \U0001F44F fitness \U0001F44F gram")

        text_input = "\n  \n 241 sucks\n\t\n    "
        self.assertEqual(gen_alternating_emoji(text_input), "\U0001F44F 241 \U0001F44F sucks")

        return


if __name__ == '__main__':
    unittest.main()
