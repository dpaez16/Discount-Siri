from pydub import AudioSegment


def convert_audio_file(file, output_format):
    """
    Converts an audio file to a differt format.

    :param file: File to be converted.
    :param output_format: Output format the file will be converted to.
    :return: Converted file name, if possible.
    """

    audio_file = AudioSegment.from_file(file)
    if audio_file is None:
        return None, "Could not open {}!".format(file)

    idx = file[::-1].find('.')
    file_name = file[:-idx - 1]
    if file_name == file:
        return None, "Could not convert {} to {}!".format(file, output_format)

    new_file_name = "{}.{}".format(file_name, output_format)

    audio_file.export(new_file_name, output_format)

    return new_file_name, ""