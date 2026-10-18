import argparse;
import asyncio;
import sys;

glob PROG: str = "jacorg",
     DEFAULT_LIMIT: int = 20;

obj Invocation {
    has command: str = "",
        action: str = "",
        repo: str = "",
        as_json: bool = False,
        limit: int = DEFAULT_LIMIT,
        query: str = "",
        text: str = "";
}

def build_parser -> argparse.ArgumentParser;

def parse_args(argv: list[str]) -> Invocation;

async def dispatch(inv: Invocation) -> int;

async def main(argv: list[str]) -> int;

with entry:__main__ {
    sys.`exit(asyncio.run(main(sys.argv[1:])));
}
