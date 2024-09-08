obj outer{
    has o1:int=9;

    obj inner{
        has i1:int=8;
    }
    can foo(){
        return 'foo';
    }
    enum color{
        red,
        green,
        blue
        }

}

with entry{
    print(outer.color.green.value);
}