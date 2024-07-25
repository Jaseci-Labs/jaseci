"""Synthetically generate the inputs and outputs for a mtllm task."""

import argparse
import contextlib
import io
import itertools
import json
import os
import re
import uuid

from jaclang import jac_import

from loguru import logger

import pandas as pd

####################################################################################################
# THIS PIECE OF CODE CAN CHANGE ON BASE ON THE TYPE OF MODEL YOU ARE USING,
# WHETHER YOU ARE USING DIFFERENT SYSTEM PROMPTS OR NOT.
with open(os.path.join(os.path.dirname(__file__), "chat_template.txt"), "r") as f:
    INPUT_TEMPLATE: str = f.read()
    INPUT_TEMPLATE_ARGS: list[str] = re.findall(r"{(.*?)}", INPUT_TEMPLATE)
    assert "input" in INPUT_TEMPLATE_ARGS, "Input Template must contain input"


def get_input_prompt(input: str) -> str:
    """Return the input prompt."""
    return INPUT_TEMPLATE.format(input=input)


with open(os.path.join(os.path.dirname(__file__), "output_template.txt"), "r") as f:
    OUTPUT_TEMPLATE: str = f.read()
    OUTPUT_TEMPLATE_ARGS: list[str] = re.findall(r"{(.*?)}", OUTPUT_TEMPLATE)
    assert "output" in OUTPUT_TEMPLATE_ARGS, "Output Template must contain output"


def get_output_prompt(output: str) -> str:
    """Return the output prompt."""
    return OUTPUT_TEMPLATE.format(output=output)


####################################################################################################


class LogCapture(contextlib.AbstractContextManager):
    """Capture log messages in a context manager."""

    def __init__(self) -> None:
        """Initialize the log capture."""
        self._log = io.StringIO()
        self._handler_id = logger.add(self._log)

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        """Remove the log handler."""
        logger.remove(self._handler_id)

    @property
    def log(self) -> io.StringIO:
        """Return the log."""
        return self._log

    def getvalue(self) -> str:
        """Return the log."""
        return self._log.getvalue()


def run(args: argparse.Namespace) -> None:
    """Run the program with different arguments and log the output."""
    # specify the program argument change logic here
    current_level_range = range(1, 100)
    level_difficulty_range = range(1, 10)

    for current_level, level_difficulty in itertools.product(
        current_level_range, level_difficulty_range
    ):

        # This would be better if we can parse aguments to like
        # jac run program.jac --current_level 1 --level_difficulty 1
        program_args = {
            "current_level": current_level,
            "level_difficulty": level_difficulty,
        }
        with open(os.path.join(args.program_dir, "program_args.json"), "w") as f:
            json.dump(program_args, f, indent=4)

        with LogCapture() as log_capture:
            try:
                jac_import(args.program, args.program_dir)
            except Exception as e:
                logger.error(e)

        with open(
            os.path.join(
                args.output_dir,
                args.output_name,
                f"log_capture_{current_level}_{level_difficulty}.log",
            ),
            "w",
        ) as f:
            f.write(log_capture.getvalue())


def read_logs(log_file: str) -> list[dict[str, str]]:
    """Read the logs and return the input and output."""
    log_list = []
    with open(log_file, "r") as f:
        logs_str = f.read()
    date = logs_str[:10]
    for log_str in logs_str.split(date):
        log_str = log_str.strip()
        if not log_str:
            continue
        search = re.search(r" - (Meaning In|Meaning Out)\n(.+)", log_str, re.DOTALL)
        if search:
            log_list.append({"type": search.group(1), "result": search.group(2)})
        else:
            log_list.append({"type": "Error", "result": log_str})
    return log_list


def filter_logs(logs: list[dict[str, str]]) -> list[dict[str, str]]:
    """Filter the logs to get the input and output as one object. skip the ones that ended with error."""
    filtered_logs = []
    # go from bottom to top
    i = len(logs) - 1
    while i >= 0:
        if logs[i]["type"] == "Meaning Out":
            filtered_logs.append(
                {"input": logs[i - 1]["result"], "output": logs[i]["result"]}
            )
            i -= 2
        elif logs[i]["type"] == "Error":
            i -= 3
        else:
            print("Unexpected log type", logs[i]["type"])
    return filtered_logs


def convert_to_dataset(args: argparse.Namespace) -> pd.DataFrame:
    """Reads the logs in the output directory and converts them to a one csv file. with input and output columns."""
    log_files = os.listdir(os.path.join(args.output_dir, args.output_name))
    logs: list[dict[str, str]] = []
    for log_file in log_files:
        logs.extend(
            read_logs(os.path.join(args.output_dir, args.output_name, log_file))
        )
    logs = filter_logs(logs)
    df = pd.DataFrame(logs)
    df["input_prompt"] = df["input"].apply(get_input_prompt)
    df["output_prompt"] = df["output"].apply(get_output_prompt)
    return df


def push_to_hf(df: pd.DataFrame, args: argparse.Namespace) -> None:
    """Push the dataset to Hugging Face."""
    from huggingface_hub import HfApi

    try:
        HfApi().create_repo(repo_id=args.repo_id, repo_type="dataset")
    except Exception as e:
        print(e)
    df.to_parquet(f"hf://datasets/{args.repo_id}/data.parquet")
    print("Dataset pushed to Hugging Face")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--program",
        type=str,
        required=True,
        help="Name of the program to run",
    )
    parser.add_argument(
        "--output_name",
        type=str,
        default=uuid.uuid4().hex,
        help="Name of the output directory",
    )
    parser.add_argument(
        "--program_dir",
        type=str,
        default=".",
        help="Directory containing the program.jac and program_args.json file",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="data_generated",
        help="Directory to write the output files",
    )
    parser.add_argument(
        "--repo_id",
        type=str,
        default=None,
        help="Hugging Face Repository ID to push the dataset to.",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(os.path.join(args.output_dir, args.output_name), exist_ok=True)

    # uncomment below line to run the program
    # run(args)
    df = convert_to_dataset(args)
    if args.repo_id:
        push_to_hf(df, args)
    df.to_csv(os.path.join(args.output_dir, args.output_name, "dataset.csv"))
