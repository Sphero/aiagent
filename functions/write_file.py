import os


def write_file(working_directory, file_path, content):
    try:
        fullpath = os.path.join(working_directory, file_path)
        working_directory = os.path.abspath(working_directory)
        target_path = os.path.abspath(fullpath)
        if not target_path.startswith(working_directory + os.sep):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
