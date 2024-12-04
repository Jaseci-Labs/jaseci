import:py os;
with entry {
  current_directory = os.path.dirname(os.path.abspath(__file__));
  input_dir = os.path.join(current_directory,'inputs/test.txt');
  print(input_dir);
  with open(input_dir, 'r') as file{
      for line in file{
          # Process each line here
          print(line.strip());  # .strip() removes trailing newlines
      }
  }
}