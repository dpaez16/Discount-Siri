from pydub import AudioSegment, exceptions


def convert_audio_file(file, output_format):
    """
    Converts an audio file to a differt format.

    :param file: File to be converted.
    :param output_format: Output format the file will be converted to.
    :return: Converted file name, if possible.
    """

    try:
        audio_file = AudioSegment.from_file(file)
    except exceptions.CouldntDecodeError:
        return None, "{} is not an appropriate audio file!".format(file)
    except FileNotFoundError:
        return None, "Could not find {}!".format(file)

    idx = file[::-1].find('.')
    if idx == -1:
        return None, "Could not convert {} to {}!".format(file, output_format)

    file_name = file[:-idx - 1]
    new_file_name = "{}_converted.{}".format(file_name, output_format)

    audio_file.export(new_file_name, output_format)

    return new_file_name, ""