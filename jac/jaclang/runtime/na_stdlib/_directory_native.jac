import from c { def opendir(path: str) -> int;  }
import from c { def readdir(dirp: int) -> int;  }
import from c { def closedir(dirp: int) -> i32;  }

def:pub directory_names(path: str) -> list[str];

def:pub try_directory_names(path: str) -> list[str];
