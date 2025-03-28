with entry {
    with open("examples/learning_section/demofile.txt", "r") as file {
        print(file.read());
    }
}

with entry {
    with open("examples/learning_section/demofile.txt") as file {
        print(file.read());
    }
}
