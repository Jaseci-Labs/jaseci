
import global_import; 
import from global_import_from {display_from, Y} 
import common; 
import last; 
import from last_from {LAST_FROM} 

can greet;


with entry{
    print('main.jac');
    greet();
    print(global_import.display_x(), global_import.X);
    print(last.LAST);
    print(LAST_FROM);
    print(display_from(), Y);
    # print(LAST_FROM2); 
}