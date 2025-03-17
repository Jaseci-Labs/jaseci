

glob common_value = 5;

include second;
include last;


with entry{
    print('common.jac');
    print(walk());
    print(LAST);
}