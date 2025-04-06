with entry {
    with open("myfile.txt", "x") as file {
        print("New file created successfully!");
    }
}

with entry {
    with open("myfile.txt", "w") as file {
        print("File created if not existing.");
    }
}
