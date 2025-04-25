"""Handle jac compile data for jaclang.org.
This script is used to handle the jac compile data for jac playground.
"""

import os
import zipfile

TARGET_FOLDER = "../../jaclang"
EXTRACTED_FOLDER = "docs/playground"
FINAL_ZIP_PATH = os.path.join(EXTRACTED_FOLDER, "jaclang.zip")
ZIP_FOLDER_NAME = "jaclang"


def pre_build_hook(**kwargs: any) -> None:
    """Run pre-build tasks for preparing files.
    This function is called before the build process starts.
    """
    print("Running pre-build hook...")
    create_final_zip()


def create_final_zip() -> None:
    """Create a zip file containing the jaclang folder.
    The zip file is created in the EXTRACTED_FOLDER directory.
    """
    print("Creating final zip...")

    if not os.path.exists(TARGET_FOLDER):
        raise FileNotFoundError(f"Folder not found: {TARGET_FOLDER}")

    with zipfile.ZipFile(FINAL_ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(TARGET_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join(
                    ZIP_FOLDER_NAME, os.path.relpath(file_path, TARGET_FOLDER)
                )
                zipf.write(file_path, arcname)

    print("Zip saved to:", FINAL_ZIP_PATH)
