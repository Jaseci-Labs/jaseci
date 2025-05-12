node Data {
  has num1: int;
  has num2: int;
}

node Result {
  has num: int;
}

node Root {}
edge async_Goto {}

walker va {
  has result:int = 0;
  can run_va_root with Root entry {
    visit [-:async_Goto:->];
  }

  can run_va with Data entry {
    self.result = here.num1 + here.num2;
    visit [-->];
  }

  can store_result with Result entry {
    here.num = self.result;
  }
}

with entry {
  r = Root();
  for i in range(10) {
    data = Data(num1 = i, num2 = i+1);
    result = Result(num=0);
    r +:async_Goto:+> data;
    data ++> result;
  }
  wlk = r spawn va();
}
