import:py os;
import:py datetime as dt;
import from math { sqrt as square_root, log }
import:jac from base_module_structure { add }
import from base_module_structure { subtract }

with entry {
    for i in range(int(square_root(dt.datetime.now().year))) {
        print(
            os.getcwd(),
            add(i, subtract(i, 1)),
            int(log(i + 1))
        );
    }
}
