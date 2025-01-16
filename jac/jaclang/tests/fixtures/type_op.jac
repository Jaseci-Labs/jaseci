node N {}
walker M {}
edge E {}
obj O {}

glob n = N();
glob m = M();
glob e = E();
glob o = O();

with entry {
    print(`root); # This prints the type of root which is Root
    print(`n); # This prints the type of n which is NodeArchitype
    print(`m); # This prints the type of m which is WalkerArchitype
    print(`e); # This prints the type of e which is EdgeArchitype
    print(`o); # This prints the type of o which is Architype
    `List;

}

can student_info(
                names: `List[str],
                hobbies: `Dict[(str, `Set[str])],
                grades: `Dict[(str, `List[int])]
                ) -> None {
    for name in names {
        print(f"{'Student: '}{name}",end='');
        print(f"{'  Hobbies: '}{', '.join(hobbies.get(name, set()))}",end='');
        print(f"{'  Grades: '}{grades.get(name, [])}");
    }
}

with entry {

    student_names = ['Alice', 'Bob', 'Charlie'];
    student_hobbies = {
        'Alice': {'Reading', 'Swimming'},
        'Bob': {'Cycling', 'Painting'},
        'Charlie': {'Gaming', 'Hiking'}
    };
    student_grades = {
        'Alice': [85, 90, 78],
        'Bob': [70, 88, 92],
        'Charlie': [95, 100, 98]
    };
    student_info(
        student_names,
        student_hobbies,
        student_grades
    );
}

node test_node {
    has value: int;
}

walker test_walker {

    can traverse with `root entry {
        visit [-->](`?test_node);
    }

    can log_visit with test_node exit {
        print(test_node,`test_node,`here,`self);
    }
}

with entry {
    for i in range(10) {
        root ++> (next:=test_node(value=i));
    }
    wlk_obj = root spawn test_walker();
    print(wlk_obj);
}