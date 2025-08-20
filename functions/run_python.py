import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
    try:
        # Resolve absolute paths
        fullpath = os.path.join(working_directory, file_path)
        abspath = os.path.abspath(working_directory)
        abspath_full = os.path.abspath(fullpath)

        # Security check: ensure file is inside working directory
        if not abspath_full.startswith(abspath + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # File existence check
        if not os.path.exists(abspath_full):
            return f'Error: File "{file_path}" not found.'

        # Ensure it's a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Run the Python script
        completed_process = subprocess.run(
            [sys.executable, abspath_full] + args,  # Python executable + script + args
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30,
        )

        # Format the output
        output_parts = []
        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr}")
        if completed_process.returncode != 0:
            output_parts.append(
                f"Process exited with code {completed_process.returncode}"
            )

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
        return f"Error: executing Python file: {e}"
