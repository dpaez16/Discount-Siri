from PIL import Image


def convert_image_file(file, output_format):
    """
    Converts an image file to a different format.

    :param file: File to be converted.
    :param output_format: Output format the file will be converted to.
    :return: Converted file name, if possible.
    """

    image_file = Image.open(file)
    if image_file is None:
        return None, "Could not open {}!".format(file)

    idx = file[::-1].find('.')
    file_name = file[:-idx - 1]
    if file_name == file:
        return None, "Could not convert {} to {}!".format(file, output_format)

    new_file_name = "{}_converted.{}".format(file_name, output_format)

    image_file.save(new_file_name)

    return new_file_name, ""