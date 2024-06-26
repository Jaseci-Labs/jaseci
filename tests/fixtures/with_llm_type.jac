import:py from mtllm.llms, BaseLLM;

obj model:BaseLLM: {
    can init(output_str: str) {
        self.verbose = False;
        self.max_tries = 1;
        self.output_str = output_str;
    }
    can __infer__(meaning_in: str, **kwargs: dict) {
        print("Meaning in: ", meaning_in);
        return f"[Output] {self.output_str}";
    }
}
glob llm1 = model(output_str="Person(name='Albert Einstein', dob='14/03/1879', age=76)");

obj 'Person'
Person {
    has name: 'Name of the Person': str,
        dob: 'Date of Birth': str,
        age: 'Age of the Person': int;
}

with entry {
    einstein: 'Einstein Object': Person = Person(name="Albert Einstein" by llm1());
    print(einstein.dob); #14/03/1879
}

glob llm2 = model(output_str="University.Department(name='Computer Science', head=Person(name='Jason Mars', dob='1994-01-01', age=30))");

obj 'University'
University {
    has name: 'Name of the University': str,
        location: 'Location of the University': str,
        departments: 'Departments in the University': list[self.Department] = [];

    obj 'Department'
    Department {
        has name: 'Name of the Department': str,
            head: 'Head of the Department': Person;
    }
}

with entry {
    umich: 'Univeristy of Michigan': University = University(name="University of Michigan", location="Ann Arbor, Michigan");
    cs_department: 'Computer Science Department': University.Department = University.Department(
        name="Computer Science" by llm2(incl_info=(umich))
    );
    print(cs_department.head); # Person(name='Jason Mars', dob='1994-01-01', age=30)

    umich.departments.append(umich.Department(name="Computer Science" by llm2()));
    print(umich.departments[0].head); # Person(name='Jason Mars', dob='1994-01-01', age=30)
}