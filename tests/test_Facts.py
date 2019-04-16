import unittest
import os
from modules.facts_meme import gen_facts_meme, fact_parser


class FactsMemeTests(unittest.TestCase):
    """
    Runs all tests to make sure that the "facts" functionality works as expected.
    """

    def test_good_input(self):
        """
        Tests to see if the "facts" functionality works as expected.
        """

        lines = fact_parser("1" * 29)
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0][-1], '-')

        lines = fact_parser("1"*28)
        self.assertEqual(len(lines), 1)
        self.assertNotEqual(lines[0][-1], '-')

        prev_dir = os.getcwd()
        os.chdir("./../")

        deep_fried, msg = gen_facts_meme("nvdio")
        self.assertTrue(msg is None)

        os.remove(deep_fried)

        os.chdir(prev_dir)

        return


if __name__ == '__main__':
    unittest.main()
