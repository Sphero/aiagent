from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

# Existing examples
# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "pkg"))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))
# print(get_file_content("calculator", "main.py"))
# print(get_file_content("calculator", "pkg/calculator.py"))
# print(get_file_content("calculator", "/bin/cat"))
# print(get_file_content("calculator", "pkg/does_not_exist.py"))
# print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
# print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
# print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
# print(run_python_file("calculator", "main.py"))
# print(run_python_file("calculator", "main.py", ["3 + 5"]))
# print(run_python_file("calculator", "tests.py"))
# print(run_python_file("calculator", "../main.py"))
# print(run_python_file("calculator", "nonexistent.py"))
# print(get_file_content("calculator", "main.py"))
# print(write_file("calculator", "main.txt", "hello"))
# print(run_python_file("calculator", "main.py"))
# print(get_files_info("calculator", "pkg"))
