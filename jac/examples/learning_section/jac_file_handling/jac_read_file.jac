with entry {
    with open("examples/learning_section/demofile.txt", "r") as file {
        print(file.read(5)); # Reads the first 5 characters
    }
}

with entry {
    with open("examples/learning_section/demofile.txt", "r") as file {
        print(file.readline()); # Reads the first line
    }
}

with entry {
    with open("examples/learning_section/demofile.txt", "r") as file {
        print(file.readline()); # Reads first line
        print(file.readline()); # Reads second line
    }
}

with entry {
    with open("examples/learning_section/demofile.txt", "r") as file {
        for line in file {
            print(line);
        }
    }
}

with entry {
    with open("examples/learning_section/demofile.txt", "r") as file {
        print(file.readline());
    }
    # File is automatically closed when the 'with' block ends

}
