walker Adder{
    can do with `<root> entry;
}

node node_a{
    has x:int = 0;
    has y:int = 0;
    can add with Adder entry;
}

:walker:Adder:can:do{
    <here> ++> node_a();

    visit -->;

}

:node:node_a:can:add{
    <self>.x= "Give a number :" |> input ;
    <self>.y= "Give a number :" |> input ;
    print(int(<self>.x) + int(<self>.y));

}
#using the A_PIPE_FWD
with entry{
    :> Adder spawn <root>;  #same as 'Adder() spawn <root>'
}