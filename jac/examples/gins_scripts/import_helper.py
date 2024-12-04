import os
def import_inputs():
  current_directory = os.path.dirname(os.path.abspath(__file__))
  input_dir = os.path.join(current_directory,'inputs/test.txt')
  inputs = []
  with open(input_dir, 'r') as file:
      for line in file:
          # Process each line here
          inputs.append[int(line.strip())]  # .strip() removes trailing newlines
  return inputs