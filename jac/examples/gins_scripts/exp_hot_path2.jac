import:py random;

with entry {
  accu:int = 0;
  itr:int = 0;
  threshold:int = 500000;
  series:list=[];
  meas:list=[0,0,0,0,0,0,0,0,0,0];
  for num in range(10) {
    series.append(num * num * num);
  }
  for i in range(len(series)) {
    while itr < 100000 {    
        accu += series[i];
        if accu < threshold {
            meas[i] += random.uniform(0.01,0.05);
        }
        else {
            meas[i] -= random.uniform(0.01,0.05);
        }
        itr += 1;
    }
  }
}