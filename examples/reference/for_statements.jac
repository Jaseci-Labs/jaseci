#Example 1

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
#Example 2
with entry{
    n=5;
    for i=1 to i <= n by i+=1{
        for j=1 to j<=n-i by j+=1{
            print("  ", end="");
        }
        for k=1 to k<=(2*i)-1 by k+=1{
            print("* ", end="");
        }
    print();
    }
}





