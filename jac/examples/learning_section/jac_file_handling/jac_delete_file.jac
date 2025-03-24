import:py os;

with entry {
    if os.path.exists("demofile.txt") {
        print("The file exists");
        os.remove("demofile.txt");
    } else {
        print("The file does not exist");
    }
}

import:py os;

with entry {
    if os.path.exists("my folder") {
        print("The folder exists");
        os.rmdir("my folder");
    } else {
        print("The folder does not exist");
    }
}
