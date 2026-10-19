"""`flow node spawn W(...)` is not a call: the node and walker are still built inside the task."""
import threading;

def where -> str {
    return threading.current_thread().name;
}

node N {}

walker W {
    has made_on: str = "";
}

with entry {
    task = flow N() spawn W(made_on=where()) ;
    print("walker built on: " + (wait task ).made_on);
}
