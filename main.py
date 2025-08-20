import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from schemas import all_schemas  # schemas for Gemini

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Available functions (all schemas)
available_functions = types.Tool(function_declarations=all_schemas)

# Dispatcher mapping: function name -> implementation
FUNCTION_MAP = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

# Working directory for sandboxed execution
WORKING_DIR = "./calculator"


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Inject working_directory
    function_args["working_directory"] = WORKING_DIR

    if function_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        result = FUNCTION_MAP[function_name](**function_args)
    except Exception as e:
        result = f"Error: Exception while running {function_name}: {e}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )


# Hardcoded system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Handle command-line arguments
args = sys.argv
if len(args) < 2:
    print("No arguments provided.")
    sys.exit(1)

user_prompt = args[1]
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
model_name = "gemini-2.0-flash"


def main():
    verbose = len(args) > 2 and args[2] == "--verbose"

    for iteration in range(20):  # max 20 iterations
        if verbose:
            print(f"\n--- Iteration {iteration+1} ---")

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
        except Exception as e:
            print(f"Fatal: Exception while calling model: {e}")
            break

        if not response.candidates:
            print("No candidates returned.")
            break

        # Take the first candidate (usually only one)
        candidate = response.candidates[0]
        messages.append(candidate.content)

        # If the model decided to call tools
        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(
                    function_call_part, verbose=verbose
                )

                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response.response
                ):
                    print("Fatal: No function response returned")
                    return

                if verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )

                # Feed result back into conversation
                messages.append(function_call_result)

        else:
            # If there’s actual text output, we’re done
            if candidate.content and candidate.content.parts:
                final_text = candidate.content.parts[0].text
                print("\nAI Final Response:")
                print(final_text)
                break

    else:
        print("Reached maximum iterations without conclusion.")


if __name__ == "__main__":
    main()
