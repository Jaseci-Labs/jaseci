
include global_include; 
include common; 
include last; 

can greet;


with entry{
    print('main.jac');
    greet();
    print(display_x(), X);
    print(LAST);
}