can foo(){
    for i in range(3){
        yield i;
        }
}

with entry{
    for i in foo(){
        print("Yielded:", i);
        }
}