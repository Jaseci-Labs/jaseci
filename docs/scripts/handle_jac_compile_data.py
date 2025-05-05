"""Handle jac compile data for jaclang.org.

This script is used to handle the jac compile data for jac playground.
"""

import os
import time
import zipfile

from jaclang.utils.lang_tools import AstTool

TARGET_FOLDER = "../../jaclang"
EXTRACTED_FOLDER = "docs/playground"
PLAYGROUND_ZIP_PATH = os.path.join(EXTRACTED_FOLDER, "jaclang.zip")
ZIP_FOLDER_NAME = "jaclang"
UNIIR_NODE_DOC = "docs/for_contributors/uniir_node.md"
LANG_REF_DOC = "docs/for_coders/jac_ref.md"
INTERNALS_DOC = "docs/for_contributors/internals.md"
AST_TOOL = AstTool()


def pre_build_hook(**kwargs: dict) -> None:
    """Run pre-build tasks for preparing files.

    This function is called before the build process starts.
    """
    print("Running pre-build hook...")
    if not os.path.exists(PLAYGROUND_ZIP_PATH):
        create_playground_zip()
    else:
        print(f"Zip file already exists: {PLAYGROUND_ZIP_PATH}. Skipping creation.")

    if is_file_older_than_minutes(UNIIR_NODE_DOC, 5):
        with open(UNIIR_NODE_DOC, "w") as f:
            f.write(AST_TOOL.autodoc_uninode())
    else:
        print(f"File is recent: {UNIIR_NODE_DOC}. Skipping creation.")

    if is_file_older_than_minutes(LANG_REF_DOC, 5):
        with open(LANG_REF_DOC, "w") as f:
            f.write(AST_TOOL.automate_ref())
    else:
        print(f"File is recent: {LANG_REF_DOC}. Skipping creation.")


def is_file_older_than_minutes(file_path: str, minutes: int) -> bool:
    """Check if a file is older than the specified number of minutes."""
    if not os.path.exists(file_path):
        return True

    file_time = os.path.getmtime(file_path)
    current_time = time.time()
    time_diff_minutes = (current_time - file_time) / 60

    return time_diff_minutes > minutes


def create_playground_zip() -> None:
    """Create a zip file containing the jaclang folder.

    The zip file is created in the EXTRACTED_FOLDER directory.
    """
    print("Creating final zip...")

    if not os.path.exists(TARGET_FOLDER):
        raise FileNotFoundError(f"Folder not found: {TARGET_FOLDER}")

    with zipfile.ZipFile(PLAYGROUND_ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(TARGET_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join(
                    ZIP_FOLDER_NAME, os.path.relpath(file_path, TARGET_FOLDER)
                )
                zipf.write(file_path, arcname)

    print("Zip saved to:", PLAYGROUND_ZIP_PATH)
