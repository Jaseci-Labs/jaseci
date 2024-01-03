with entry{
    d=[2,3,4,5,6,7,8];

    can count_odds(data : list) -> int {
         odds=[o for o in data if o%2 ==1];
         return len(odds);
    }

    if (n := count_odds(d))>1{
        print(f"{n} odds");
    }


}