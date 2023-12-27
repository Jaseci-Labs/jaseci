import os


def extract_headings(file_path: str) -> dict[str, tuple[int, int]]:
    with open(file_path, "r") as file:
        lines = file.readlines()
    h = []
    current_heading = None
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("//"):
            if current_heading is not None:
                h.append(current_heading)
            current_heading = line.strip()[2:]
    if current_heading is not None:
        h.append(current_heading)
    return h


def convert_to_snake_case(name):
    # Convert the name to snake_case and replace '/' with '_'
    snake_case_name = name.lower().replace("/", "_").replace("-", "_").replace(" ", "_")
    return snake_case_name


headings8 = extract_headings("jac.lark")
# print(headings8)
# # Convert names to snake_case and replace '/' with '_'
snake_case_headings = [convert_to_snake_case(name.strip()) for name in headings8]

# # Display the result
print(snake_case_headings)
print(len(snake_case_headings))
# List of file names to check or create


# Directory path where the files should be located
directory_path = os.getcwd()
print(directory_path)
# # Iterate through the list of file names
for x in snake_case_headings:
    pythonfile_name = x + ".py"
    jacfile_name = x + ".jac"
    pythonfile_path = os.path.join(directory_path, pythonfile_name)
    jacfile_path = os.path.join(directory_path, jacfile_name)

    # Check if the python file already exists
    if not os.path.exists(pythonfile_path):
        # Create an empty file if it doesn't exist
        with open(pythonfile_path, "w"):
            pass
        print(f"File '{pythonfile_path}' created.")
    else:
        print(f"File '{pythonfile_path}' already exists.")

    # Check if the jac file already exists
    if not os.path.exists(jacfile_path):
        # Create an empty file if it doesn't exist
        with open(jacfile_path, "w"):
            pass
        print(f"File '{jacfile_path}' created.")
    else:
        print(f"File '{jacfile_path}' already exists.")

# # Optional: Display the list of files in the directory after the operation
print("Files in the directory:", os.listdir(directory_path))
