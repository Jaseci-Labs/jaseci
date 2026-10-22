"""A print into a with-bound file would replay after the file closes, so it stays
eager; a print to sys.stderr is still buffered."""
import sys;
import torch;

@torch.compile()
def to_file(x: any, path: str) -> any {
    x = torch.relu(x);
    with open(path, "w") as fh {
        print("GM-FILE", file=fh);
    }
    return x * 2.0;
}

@torch.compile()
def to_stderr(x: any) -> any {
    x = torch.relu(x);
    print("GM-ERR", file=sys.stderr);
    return x * 2.0;
}
