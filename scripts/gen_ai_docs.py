import sys
import shutil
from os import walk
import os
from os.path import exists


root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ai_kit_root = root + "/jaseci_ai_kit/"
print(ai_kit_root)
output_path = os.path.join(root, "docs/docs/jaseci_ai_kit")  # no trailing slash

toc_path = os.path.join(root, "README.md")


def main():

    if not os.path.exists(toc_path):
        sys.exit()

    # remove output directory if it exists
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    # generate output directory (if it doesn't exist)
    os.makedirs(output_path)
    shutil.copy(root + "/jaseci_ai_kit/README.md", output_path + "/introduction.md")

    os.makedirs(output_path + "/jac_nlp")
    shutil.copy(
        root + "/jaseci_ai_kit/jac_nlp/README.md",
        output_path + "/jac_nlp/introduction.md",
    )
    copy_mds(ai_kit_root + "/jac_nlp", output_path + "/jac_nlp")

    os.makedirs(output_path + "/jac_misc")
    shutil.copy(
        root + "/jaseci_ai_kit/jac_misc/README.md",
        output_path + "/jac_misc/introduction.md",
    )
    copy_mds(ai_kit_root + "/jac_misc", output_path + "/jac_misc")

    os.makedirs(output_path + "/jac_speech")
    shutil.copy(
        root + "/jaseci_ai_kit/jac_speech/README.md",
        output_path + "/jac_speech/introduction.md",
    )
    copy_mds(ai_kit_root + "/jac_speech", output_path + "/jac_speech")

    os.makedirs(output_path + "/jac_vision")
    shutil.copy(
        root + "/jaseci_ai_kit/jac_vision/README.md",
        output_path + "/jac_vision/introduction.md",
    )
    copy_mds(ai_kit_root + "/jac_vision", output_path + "/jac_vision")

    print("Copied ai_kit_docs directories")


def copy_mds(origin, destination):
    for root, dirs, files in os.walk(origin):
        for file in files:
            if file[-3:].lower() == ".md":
                dest_file_name = str(root).split("/")[-1] + ".md"

                if (
                    dest_file_name == "jac_nlp.md"
                    or dest_file_name == "jac_misc.md"
                    or dest_file_name == "jac_speech.md"
                    or dest_file_name == "jac_vision.md"
                ):
                    pass
                else:
                    shutil.copy(
                        os.path.join(root, file),
                        os.path.join(destination, dest_file_name),
                    )


main()
