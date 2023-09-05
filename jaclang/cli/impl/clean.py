import os
import shutil


def clean():
    current_directory = os.getcwd()  # Get the current working directory
    jac_gen = "__jac_gen__"
    py_cache = "__pycache__"
    for root, dirs, files in os.walk(current_directory, topdown=False):
        for folder_name in dirs[:]:
            if folder_name == jac_gen or folder_name == py_cache:
                folder_to_remove = os.path.join(root, folder_name)
                shutil.rmtree(folder_to_remove)
                print(f"Removed folder: {folder_to_remove}")

    print("Done cleaning.")


clean()
