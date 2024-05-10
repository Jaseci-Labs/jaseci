import:py os;
with entry{
    print("Hello World");
    print(os.getcwd());
}
# import:py tensorflow as tf;
# with entry{
#     print("Hello World");
#     print(tf.__version__);
# }


import:py random;
with entry{

    can entry(){
    print("Hello World");
    print(random.randint(0, 100));

    # Generate random numbers
    print(random.random()) ;
    print(random.uniform(1, 10)) ;
    print(random.randint(1, 6)) ;
    print(random.randrange(1, 10, 2)) ;

    # Sequence operations
    colors = ['red', 'green', 'blue', 'yellow', 'orange'];
    print(random.choice(colors)) ; # Random color from the list
    print(random.sample(colors, 3));  # Random sample of 3 colors from the list
    random.shuffle(colors);
    print(colors);  # Colors shuffled in-place

    # Distributions
    print(random.normalvariate(0, 1));  # Random sample from a normal distribution with mean 0 and stddev 1
    print(random.lognormvariate(0, 1)) ; # Random sample from a log-normal distribution with mean 0 and stddev 1

    # Seed and state
    random.seed(42) ;
    print(random.random()) ;
    state = random.getstate()  ;
    random.setstate(state) ;
    print(random.random()) ;


    print('\n\nyou clicked me\n\n');
    }
}


# tkinter
import:py tkinter as tk;
with entry{
    __root__ = tk.Tk();
    __root__.title("Random Module Example");

    button = tk.Button(__root__, text="Click Me", command=entry);
    button.pack(pady=20);
    __root__.mainloop();


    # root0 = tk.Tk();

    # menu_bar = tk.Menu(root0);
    # file_menu = tk.Menu(menu_bar);
    # file_menu.add_command(label="New");
    # file_menu.add_command(label="Open");
    # file_menu.add_separator();
    # file_menu.add_command(label="Exit", command=root0.quit);
    # menu_bar.add_cascade(label="File", menu=file_menu);

    # root0.config(menu=menu_bar);
    # root0.mainloop();

}









# import:py maze;


# with entry {
#     root_ = tk.Tk();
#     equation = "";
# }

# can show(value: Any) {
#     :global: equation ;
#     equation += value;
#     result.config(text=equation) ;
# }

# can clear() {
#     :global: equation ;
#     equation = "";
#     result.config(text=equation) ;
# }

# can calculate() {
#     :global: equation ;

#     try  {
#         result.config(text=str(eval(equation))) ;} except Exception as e {
#         result.config(text="Error") ;
#     }

#     equation = "";
# }

# with entry {
#     result = tk.Label(root_, text="");
#     result.grid(row=0, column=0, columnspan=4) ;
#     button_1 = tk.Button(root_, text="1", command=with  can show("1"));
#     button_1.grid(row=1, column=0) ;
#     button_2 = tk.Button(root_, text="2", command=with  can show("2"));
#     button_2.grid(row=1, column=1) ;
#     button_clear = tk.Button(root_, text="C", command=clear);
#     button_clear.grid(row=4, column=0) ;
#     button_equal = tk.Button(root_, text="=", command=calculate);
#     button_equal.grid(row=4, column=3) ;
#     root_.mainloop() ;
# }