import sys
import shutil
import os
from os.path import exists


root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ai_kit_root = root + "/jaseci_ai_kit/"
output_path = os.path.join(
    root, "docs/docs/tutorials/jaseci_ai_kit"
)  # no trailing slash

toc_path = os.path.join(root, "README.md")


def main():

    # remove output directory if it exists
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    # generate output directory (if it doesn't exist)
    os.makedirs(output_path)
    shutil.copy(
        os.path.join(ai_kit_root, "_category_.json"),
        os.path.join(output_path, "_category_.json"),
    )

    os.makedirs(output_path + "/jac_nlp")
    shutil.copy(
        os.path.join(ai_kit_root + "/jac_nlp", "_category_.json"),
        os.path.join(output_path + "/jac_nlp/" + "_category_.json"),
    )
    copy_mds(ai_kit_root + "/jac_nlp", output_path + "/jac_nlp")

    os.makedirs(output_path + "/jac_misc")
    shutil.copy(
        os.path.join(ai_kit_root + "/jac_misc", "_category_.json"),
        os.path.join(output_path + "/jac_misc/" + "_category_.json"),
    )
    copy_mds(ai_kit_root + "/jac_misc", output_path + "/jac_misc")

    os.makedirs(output_path + "/jac_speech")
    shutil.copy(
        os.path.join(ai_kit_root + "/jac_speech", "_category_.json"),
        os.path.join(output_path + "/jac_speech/" + "_category_.json"),
    )
    copy_mds(ai_kit_root + "/jac_speech", output_path + "/jac_speech")

    os.makedirs(output_path + "/jac_vision")
    shutil.copy(
        os.path.join(ai_kit_root + "/jac_vision", "_category_.json"),
        os.path.join(output_path + "/jac_vision/" + "_category_.json"),
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
            elif file[-4:].lower() == ".png":
                img_dest = destination + "/img"
                if not os.path.exists(img_dest):
                    os.makedirs(img_dest)
                shutil.copy(
                    os.path.join(root, file),
                    os.path.join(img_dest, file),
                )


main()
