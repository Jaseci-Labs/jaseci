obj mainObject;

:obj:mainObject{
    can greet;
    obj subObject;
}
can foo{
     obj kk;
     return kk();
}
:can:foo:obj:kk{
    can bar{
        print("Hello,from bar in kk");
    }
}

with entry{
    foo().bar();
}
:obj:mainObject:can:greet{
    print("Greeting: Hello, World!");
}

:obj:mainObject:obj:subObject{
    can displayMessage;
    can shortMessage{
        print("Hello, World!");
    }
    obj nestedObject;
}
:obj:mainObject:obj:subObject:can:displayMessage{
    print("Repeated: Hello!");
}

:obj:mainObject:obj:subObject:obj:nestedObject{
    can lastMessage;
    can finalMessage{
        print("Final message:!");
    }
}

:obj:mainObject:obj:subObject:obj:nestedObject:can:lastMessage{
# impl mainObject.subObject.nestedObject{  # TODO
        print("Last message:!");

}


with entry{
    mainObject().greet();
    mainObject().subObject().displayMessage();
    mainObject().subObject().shortMessage();
    mainObject().subObject().nestedObject().lastMessage();
    mainObject().subObject().nestedObject().finalMessage();
}