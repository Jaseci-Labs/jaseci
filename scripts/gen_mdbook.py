# pylint: disable=unused-variable
# compiles all markdown docs across repo and generates mdbook rendered documentation

import sys
import shutil
from os import walk
import os
from os.path import exists
import subprocess

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
output_path = os.path.join(root, "mdbook")  # no trailing slash
theme_source_path = os.path.join(root, "support/mdbook_theme")  # no trailing slash
toc_path = os.path.join(root, "README.md")

def extract_content_below_title(markdown_file, title, output_file):
    """
    Extracts all content below the given title in the Markdown file and writes it to the output file.
    """
    with open(markdown_file, "r") as f:
        lines = f.readlines()

    start_index = None
    for i, line in enumerate(lines):
        if line.strip() == f"## {title}":
            start_index = i + 1
            break

    if start_index is None:
        raise ValueError(f"Title '{title}' not found in file {markdown_file}")

    with open(output_file, "w") as f:
        f.writelines(lines[start_index:])





def pluck_content_below_title(title, input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    found_title = False
    with open(output_file, "w") as f:
        for line in lines:
            if found_title:
                if line.startswith("##"):
                    break
                f.write(line)
            elif line.startswith("## " + title):
                found_title = True
                f.write(line)


def main():
    # ensure main TOC readme exists before continuing
    if not os.path.exists(toc_path):
        sys.exit()

    # remove output directory if it exists
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    # generate output directory (if it doesn't exist)
    os.makedirs(output_path)
    os.makedirs(output_path + "/src")

    # build SUMMARY.md based on README.md
    print(1)
    build_summary_file()

    # init mdbook
    print(2)

    init_mdbook()

    # booktool
    print(3)

    generate_booktool_cheatsheet()
    generate_booktool_stdlib()
    generate_booktool_class()

    # copy theme
    import_theme()

    # build mdbook
    build_mdbook()


def build_summary_file():
    readme = ""
    if not os.path.exists(toc_path):
        sys.exit()

    # generate the SUMMARY.md file (if it doesn't exist)
    with open(output_path + "/src/SUMMARY.md", "w+") as summaryfile:
        summaryfile.write("")
        summaryfile.write("# summary \n")

    # start processing the README.md, build the SUMMARY.md, transfer assets
    with open(toc_path, "r") as readme:
        lines = readme.readlines()

    for line in lines:
        if line.find(".md#") != -1:
            space = line.split("-")[0]
            title = line.split("#")[0]
            title = title.split("[")[1]
            title = title.split("]")[0]
            path = line.split("#")[0]
            path = path.split("(")[1]
            new_file_name = line.split("#")[1]
            new_file_name = new_file_name.split(")")[0]
            new_file_name = new_file_name.replace("-", "_")
            new_file_name = new_file_name+".md"
            new_file_name = new_file_name.replace(" ", "")
            file_reference = new_file_name
            new_file_name = os.path.join("./mdbook/src",new_file_name)
            extract_content_below_title(
                path, title, new_file_name
            )
            template_syntax = f"- [{title}]({file_reference})"
            template_syntax = space+template_syntax

            with open(output_path + "/src/SUMMARY.md", "a") as summaryfile:
                summaryfile.write(template_syntax + "\n")

            pluck_content_below_title(
                title, path, new_file_name
            )

            continue

        if line.find("https") != -1:
            continue

        if line.find("##") != -1:
            line = line.replace("#", "", 1)
            with open(output_path + "/src/SUMMARY.md", "a") as summaryfile:
                summaryfile.write(line + "\n")

        else:
            with open(output_path + "/src/SUMMARY.md", "a") as summaryfile:
                summaryfile.write(line)

            fileinfo = process_line(line)
            if fileinfo is not False:
                doc_file_link = output_path + "/src/" + fileinfo["link"]
                with open(os.path.join(root, fileinfo["link"]), "r") as repofile:
                    repo_file_lines = repofile.readlines()

                filename_index = doc_file_link.rfind("/")
                folder_path = doc_file_link[0:filename_index]
                if not exists(folder_path):
                    os.makedirs(folder_path)

                with open(doc_file_link, "a+") as docfile:
                    for rf_line in repo_file_lines:
                        docfile.write(rf_line)

    # list of all image folders . Add relative path here to include images in mdbook
    imageFiles = [
        "docs/docs/examples_and_tutorials/CanoniAnalytics/images",
        "examples/CanoniCAI/images",
        "support/guide/assets",
        "support/codelabs/canonicai/images",
        "examples/CanoniCAI/codelabs/lang_docs/images",
        "jaseci_ai_kit/jaseci_ai_kit/modules/ph/assets",
        "jaseci_core/svc/",
        "support/codelabs/",
        "docs/docs/examples_and_tutorials/CanoniCAI/images",
    ]
    for images in imageFiles:
        files = get_images(os.path.join(root, images))
        import_assets(files)


def process_line(line):
    beginheading = line.find("[")
    endheading = line.find("]")

    heading = line[2 + 1 : 21]
    heading = line[beginheading + 1 : endheading]
    beginlink = line.find("(")
    endlink = line.find(")")
    if endlink == -1:
        return False

    link = line[beginlink + 1 : endlink]
    if link.find("https") != -1:
        return False
    return {"heading": heading, "link": link}


def import_assets(files):
    for file in files:
        common_path = os.path.commonprefix([output_path, file])
        relative_path = file.replace(common_path, "")
        asset_path = output_path + "/src/" + relative_path

        filename_index = asset_path.rfind("/")
        folder_path = asset_path[0:filename_index]
        if not exists(folder_path):
            os.makedirs(folder_path)

        shutil.copy(file, asset_path)


# get image paths
def get_images(path=None):
    if path != None:
        f = []
        d = []
        x = 0
        for dirpath, dirnames, filenames in walk(path):
            while x < len(filenames):
                filenames[x] = path + "/" + filenames[x]
                x = x + 1
            f.extend(filenames)
            d.extend(dirnames)
            break

        if len(d) > 0:
            for directory in d:
                image_directory = get_images(path + "/" + directory)
                f.extend(image_directory)

        return f
    return False


def init_mdbook():
    print(output_path)
    subprocess.call(
        [
            "mdbook",
            "init",
            output_path,
            "--ignore=none",
            "--title=Jaseci Docs and Guides",
        ]
    )
    # edit the toml file
    with open(output_path + "/book.toml", "a") as book:
        book.write('description = "Jaseci Documentation and Guides"\n')
        book.write("[build]\n")
        book.write("use-default-preprocessors = false\n")
        book.write("[preprocessor.links]\n")
        book.write("[output.html]\n")
        book.write('default-theme = "light"\n')
        book.write('preferred-dark-theme = "coal"\n')
        book.write("[output.html.fold]\n")
        book.write("enable = true\n")
        book.close()


def build_mdbook():
    subprocess.call(["mdbook", "build", output_path])


def generate_booktool_cheatsheet():
    print(root)
    subprocess.call(
        [
            "jsctl",
            "booktool",
            "mdcheatsheet",
            "--output",
            "support/guide/other/cheatsheet.md",
        ]
    )


def generate_booktool_stdlib():
    subprocess.call(
        ["jsctl", "booktool", "mdstdlib", "--output", "support/guide/other/stdlib.md"]
    )


def generate_booktool_class():
    subprocess.call(
        ["jsctl", "booktool", "mdclasses", "--output", "support/guide/other/classes.md"]
    )


def clean_mdbook():
    subprocess.call(["mdbook", "clean", output_path])


def import_theme():
    if not os.path.exists(output_path + "/theme"):
        os.makedirs(output_path + "/theme")

    if not os.path.exists(output_path + "/theme/css"):
        os.makedirs(output_path + "/theme/css")

    files = get_images(theme_source_path)

    for file in files:
        dest = output_path + "/theme/" + file.replace(theme_source_path + "/", "")
        source = theme_source_path + "/" + file.replace(theme_source_path + "/", "")
        shutil.copy(source, dest)


main()
