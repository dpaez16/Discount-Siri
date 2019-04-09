import unittest
from modules.front_page_preview import get_front_page_preview


class RandomFactTests(unittest.TestCase):
    """
    Runs all tests to make sure that the front page preview function works as expected.
    """

    def test_proper_format(self):
        """
        Tests to see if the front page preview function works as expected.
        """

        front_page_preview = get_front_page_preview()
        self.assertEqual(len(front_page_preview), 20)

        for post in front_page_preview:
            self.assertTrue('subreddit' in post)
            self.assertTrue('title' in post)
            self.assertTrue('preview_url' in post)
            self.assertTrue('post_link' in post)
            self.assertTrue('upvotes' in post)

            self.assertTrue("r/" in post['subreddit'])
            self.assertTrue("https://www.reddit.com" in post['post_link'])
        return


if __name__ == '__main__':
    unittest.main()
