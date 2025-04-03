# file2.jac
import:jac file1;

with entry {
    print(file1.num2); # Cannot access 'num2', it is private to 'file1.jac'
}