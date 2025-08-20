import os


def get_files_info(working_directory, directory="."):
    fullpath = os.path.join(working_directory, directory)
    abspath = os.path.abspath(working_directory)
    abspath_full = os.path.abspath(fullpath)
    if not abspath_full.startswith(abspath):
        return f'Error: "{directory}" is not a subdirectory of "{working_directory}"'
    if not os.path.isdir(abspath_full):
        return f'Error: "{directory}" is not a directory'
    dircontent = list(os.listdir(fullpath))
    result = f"Result for directory '{directory}':\n"
    if directory == ".":
        result = f"Result for current directory:\n"
    for f in dircontent:
        size = os.path.getsize(os.path.join(abspath_full, f))
        is_dir = os.path.isdir(os.path.join(abspath_full, f))
        result += f"- {f}: file_size={size}, is_dir={is_dir}\n"
    return result
