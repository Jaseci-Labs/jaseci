import:py os;
import:py random;

with entry {
  current_directory = os.path.dirname(os.path.abspath(__file__));
  input_dir = os.path.join(current_directory,'inputs/test.txt');

  var = [];
  with open(input_dir, 'r') as file {
      for line in file {
          # Process each line here
          var.append(float(line.strip()));  # .strip() removes trailing newlines
      }
  }
  a:int = 0;
  b:int = 0;
  c:int = 0;
  input_val:float = 0.0;
  test_val: float = 0.0;
  count:int = 0;
  accum_sum:float = 0.0;
  changing_average:float = 0;
  change_reduction_arr:list=[];
  for val in var {
    input_val = val;
    count = count + 1;
    accum_sum = accum_sum + val;
    changing_average = accum_sum/count;
    if (changing_average)/100 < 1.0 {
      test_val:int = test_val + 100.0;
    }
    else {
      for i in range(count) {
        test_val = test_val + 10.0;
      }
    }
  }
  while test_val > 0 {
    reduce:float = random.uniform(5.0,10.0);
    test_val -= 100.0;
    # change_reduction_arr.append(test_val);
  }
}