import unittest
from modules.definition import get_definition


class DefinitionTests(unittest.TestCase):
    """
    Runs all tests to make sure that the definition functionality works as expected.
    """

    def test_bad_words(self):
        """
        Tests to see if the definition function catches "bad words" properly.
        """

        full_definition, msg = get_definition("")
        self.assertFalse(msg is None)

        full_definition, msg = get_definition("asdfda")
        self.assertFalse(msg is None)

        full_definition, msg = get_definition("qeroiqwe8yr213")
        self.assertFalse(msg is None)

        return

    def test_good_words(self):
        """
        Tests to see if the definition function catches "good words" properly.
        """

        full_definition, msg = get_definition("word")
        self.assertTrue(msg is None)

        full_definition, msg = get_definition("ace")
        self.assertTrue(msg is None)

        full_definition, msg = get_definition("bop")
        self.assertTrue(msg is None)

        return


if __name__ == '__main__':
    unittest.main()
