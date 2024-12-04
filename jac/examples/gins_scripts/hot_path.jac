import:py os;

can import_inputs() {
  current_directory = os.path.dirname(os.path.abspath(__file__));
  input_dir = os.path.join(current_directory,'inputs/test.txt');
  with open(input_dir, 'r') as file {
      for line in file {
          # Process each line here
          print(line.strip());  # .strip() removes trailing newlines
      }
  }
}


with entry {
  a:int = 0;
  b:int = 0;
  c:int = 0;
  in_vals:list[int] = import_inputs();
  while a < 30000 {
    if a % 2 == 0{
      c = a+b+7;
      
    }
    else {
      b = 2 + c;
    }
    a += 1;
  }
}