obj mainObject;

impl obj mainObject{
    def greet;
    obj subObject;
}
def foo{
     obj ObjInsideFunction;
     return ObjInsideFunction();
}
impl obj foo.ObjInsideFunction{
    def bar{
        print("Hello,from bar in kk");
    }
}

with entry{
    foo().bar();
}
impl def mainObject.greet{
    print("Greeting: Hello, World!");
}

impl obj mainObject.subObject{
    def displayMessage;
    def shortMessage{
        print("Hello, World!");
    }
    obj nestedObject;
}
impl def mainObject.subObject.displayMessage{
    print("Repeated: Hello!");
}

impl obj mainObject.subObject.nestedObject{
    def lastMessage;
    def finalMessage{
        print("Final message:!");
    }
}

impl def mainObject.subObject.nestedObject.lastMessage{
        print("Last message:!");

}


with entry{
    mainObject().greet();
    mainObject().subObject().displayMessage();
    mainObject().subObject().shortMessage();
    mainObject().subObject().nestedObject().lastMessage();
    mainObject().subObject().nestedObject().finalMessage();
}