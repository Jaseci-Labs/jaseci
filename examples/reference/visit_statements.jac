walker Creator {
    can create with `<root> entry;
    can stop with `<root> entry;
    }

node item{
    can print_something with Creator entry{
        print("Hey There!!!");

    }
}

:walker:Creator:can:create{
    for i=0 to i < 5 by i+=1{
        <here> ++> item();

    }
    visit-->else{
        visit <root>;
    }
}

:walker:Creator:can:stop{
    print("walking stopped");
    disengage;
    }

with entry{
    <root> spawn Creator();
}

