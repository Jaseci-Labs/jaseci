#Open file
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

#Read Files

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

#Create a New File

with entry {
    with open("my_file.txt", "x") as file {
        print("New file created successfully!");
    }
}

with entry {
    with open("my_file.txt", "w") as file {
        print("File created if not existing.");
    }
}

#Write a File

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

# Delete File

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
