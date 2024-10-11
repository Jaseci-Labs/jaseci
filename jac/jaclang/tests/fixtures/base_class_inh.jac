
import:py from base_class_py {A}
class B :A: {}

with entry {
    l = A();
    b = B();
    print(b.start());
}