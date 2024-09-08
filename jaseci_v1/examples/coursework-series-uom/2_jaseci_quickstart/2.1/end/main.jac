import {*} with "./graph.jac";

walker run {
    root {
        family_tree = spawn here ++> graph::family_tree;
        father = spawn node::person(
            id = "6743482333V",
            name = "John",
            date_of_birth = "1967-01-01",
            profession = "Engineer",
            gender = "Male"
        );
        family_tree ++> father;
        mother = spawn node::person(
            id = "694343433V",
            name = "Mary",
            date_of_birth = "1969-01-01",
            profession = "Architecture",
            gender = "Female"
        );
        family_tree ++> mother;
        father <+[married]+> mother;
        son = spawn node::person(
            id = "9643482333V",
            name = "George",
            date_of_birth = "1996-01-01",
            profession = "Student",
            gender = "Male"
        );
        family_tree ++> son;
        father +[child]+> son;
        mother +[child]+> son;
    }
}