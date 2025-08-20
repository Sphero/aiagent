import os

from functions.config import MAX_FILE_CONTENT_LENGTH as maxlength


def get_file_content(working_directory, file_path):
    fullpath = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(working_directory)
    abspath_full = os.path.abspath(fullpath)
    if not abspath_full.startswith(abspath):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abspath_full):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(abspath_full, "r", encoding="utf-8") as file:
        content = file.read(maxlength)
    if len(content) > maxlength:
        content = (
            content[:maxlength]
            + f'\n[...File "{file_path}" truncated at {maxlength} characters]'
        )
    return content
