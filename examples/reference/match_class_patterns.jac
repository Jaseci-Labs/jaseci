obj Point {
    has x: flaot, y: float;
}
with entry{
    data=Point(x=9,y=0);

    match data { 
        
        # MatchClass
        case Point(int(a), y=0):
            print(f"Point with x={a} and y=0");
    }
 }