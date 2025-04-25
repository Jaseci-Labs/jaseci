import os
import zipfile
import shutil
import subprocess

REPO_GIT_URL = "https://github.com/Jaseci-Labs/jac_playground.git"
CLONE_DIR = "temp_repo"
TARGET_FOLDER_INSIDE_REPO = "jaclang"
EXTRACTED_FOLDER = "docs/playground"
FINAL_ZIP_PATH = os.path.join(EXTRACTED_FOLDER, "jaclang.zip")

def pre_build_hook(**kwargs):
    print("Running pre-build hook...")
    clone_repo()
    create_final_zip()
    clean_temp()

def clone_repo():
    print("Cloning GitHub repository...")
    subprocess.run(["git", "clone", REPO_GIT_URL, CLONE_DIR], check=True)

def create_final_zip():
    print("Creating final zip...")

    folder_to_zip = os.path.join(CLONE_DIR, TARGET_FOLDER_INSIDE_REPO)

    if not os.path.exists(folder_to_zip):
        raise FileNotFoundError(f"Folder not found: {folder_to_zip}")

    with zipfile.ZipFile(FINAL_ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_to_zip)
                zipf.write(file_path, arcname)

    print("Zip saved to:", FINAL_ZIP_PATH)

def clean_temp():
    print("Cleaning up...")
    shutil.rmtree(CLONE_DIR, ignore_errors=True)

