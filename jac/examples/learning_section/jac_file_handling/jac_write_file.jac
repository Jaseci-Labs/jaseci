with entry {
    with open("examples/learning_section/demofile.txt", "a") as file {
        file.write("Now the file has more content!\n");
    }

    # Open and read the file after appending
    with open("examples/learning_section/demofile.txt", "r") as file {
        print(file.read());
    }
}

with entry {
    with open("examples/learning_section/demofile.txt", "w") as file {
        file.write("Woops! I have deleted the content!\n");
    }

    # Open and read the file after overwriting
    with open("examples/learning_section/demofile.txt", "r") as file {
        print(file.read());
    }
}
