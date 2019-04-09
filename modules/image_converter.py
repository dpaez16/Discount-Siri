from PIL import Image


def convert_image_file(file, output_format):
    """
    Converts an image file to a different format.

    :param file: File to be converted.
    :param output_format: Output format the file will be converted to.
    :return: Converted file name, if possible.
    """

    try:
        image_file = Image.open(file)
    except FileNotFoundError:
        return None, "Could not find {}!".format(file)
    except OSError:
        return None, "{} is not an appropriate image file!".format(file)

    idx = file[::-1].find('.')
    if idx == -1:
        return None, "Could not convert {} to {}!".format(file, output_format)

    file_name = file[:-idx - 1]
    new_file_name = "{}_converted.{}".format(file_name, output_format)

    image_file.save(new_file_name)

    return new_file_name, ""
