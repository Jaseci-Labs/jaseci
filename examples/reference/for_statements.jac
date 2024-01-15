with entry{
    start_range = 1;
    end_range = 5;

    for i in range(start_range, end_range + 1){
        for number = 1 to number<=10 by number+=1{
            product = i * number;
            print(f"{i} x {number} = {product}");
        }
        print("\n", end="");
    }

}






