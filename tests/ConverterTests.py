import unittest
import os
from modules.image_converter import convert_image_file
from modules.audio_converter import convert_audio_file


class ConverterTests(unittest.TestCase):
    """
    Runs all tests to make sure that all converter functionality works as expected.
    """

    def test_bad_files(self):
        """
        Tests to see if the converter functions catch bad files properly.
        """

        prev_dir = os.getcwd()
        os.chdir("./test_files")

        output_format = "png"
        file = "not_a_file.com"
        converted, msg = convert_image_file(file, output_format)
        self.assertNotEqual(msg, "")

        converted, msg = convert_audio_file(file, output_format)
        self.assertNotEqual(msg, "")

        file = "also_not_a_file"
        converted, msg = convert_image_file(file, output_format)
        self.assertNotEqual(msg, "")

        converted, msg = convert_audio_file(file, output_format)
        self.assertNotEqual(msg, "")

        file = "nan"
        converted, msg = convert_image_file(file, output_format)
        self.assertNotEqual(msg, "")

        converted, msg = convert_audio_file(file, output_format)
        self.assertNotEqual(msg, "")

        os.chdir(prev_dir)

        return

    def test_good_file(self):
        """
        Tests to see if the converter functions catch good files properly.
        """

        prev_dir = os.getcwd()
        os.chdir("./test_files")

        output_format = "png"
        file = "firewatch.jpg"
        converted1, msg = convert_image_file(file, output_format)
        self.assertEqual(msg, "")

        output_format = "wav"
        file = "SampleAudio.mp3"
        converted2, msg = convert_audio_file(file, output_format)
        self.assertEqual(msg, "")

        os.remove(converted1)
        os.remove(converted2)
        os.chdir(prev_dir)

        return


if __name__ == '__main__':
    unittest.main()
