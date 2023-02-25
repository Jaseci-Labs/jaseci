import re


def deconstruct_error_message(error_message):
    pattern = re.compile(r"^.*:\sline\s(\d+):(\d+)\s-\s(.+)$")

    match = pattern.match(error_message)

    if match:
        line_number = match.group(1)
        column_number = match.group(2)
        error_text = match.group(3)

        return (
            int(line_number),
            int(column_number),
            error_text,
        )

    return None
