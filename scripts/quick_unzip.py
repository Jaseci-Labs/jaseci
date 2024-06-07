import os
import tarfile
import zipfile


def extract_files(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if tarfile.is_tarfile(item_path):
            with tarfile.open(item_path, "r:*") as tar:
                tar.extractall(path=directory)
        elif zipfile.is_zipfile(item_path):
            with zipfile.ZipFile(item_path, "r") as zip_ref:
                zip_ref.extractall(directory)


extract_files("jaclang/_vendor")
