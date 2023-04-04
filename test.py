import os


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


extract_content_below_title(
    "docs/docs/development/1_abstractions.md", "Graphs", "testing.md"
)


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


pluck_content_below_title(
    "Graphs", "docs/docs/development/1_abstractions.md", "testing.md"
)
