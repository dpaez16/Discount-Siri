import unittest
from modules.image_converter import convert_image_file
from modules.audio_converter import convert_audio_file


class ConverterTests(unittest.TestCase):
    """
    Runs all tests to make sure that all converter functionality works as expected.
    """

    def test_bad_files(self):
        """
        Tests to see if the converter functions catch bad locations properly.
        """

        output_format = "png"
        file = "not_a_file.com"
        converted, msg = convert_image_file(file, output_format)
        self.assertNotEqual(msg, "")

        converted, msg = convert_audio_file(file, output_format)
        self.assertNotEqual(msg, "")

        file = "also_not_a_file"
        converted, msg = convert_image_file(file, output_format)
        self.assertNotEqual(msg, "")

        file = "also_not_a_file"
        converted, msg = convert_audio_file(file, output_format)
        self.assertNotEqual(msg, "")

        return


if __name__ == '__main__':
    unittest.main()
