# Understanding the actions by example

## Basic action example

Jaseci has set of inbuilt actions. Also you can load and unload actions in `jsctl` shell. to see the available actions in jaseci session try running `actions list`. Here are two basic example of jaseci `date` actions.

**Example 1:**

```jac
node person {
    has name;
    has birthday;
}

walker init {
    can date.quantize_to_year;
    can date.quantize_to_month;
    can date.quantize_to_week;

    person1 = spawn here ++> node::person(name="Josh", birthday="1995-05-20");

    birthyear = date.quantize_to_year(person1.birthday);
    birthmonth = date.quantize_to_month(person1.birthday);
    birthweek = date.quantize_to_week(person1.birthday);

    std.out("Date ", person1.birthday);
    std.out("Quantized date to year ", birthyear);
    std.out("Quantized date to month ", birthmonth);
    std.out("Quantized date to week ", birthweek);
}
```
**Output 1:**
```
Date  1995-05-20
Quantized date to year  1995-01-01T00:00:00
Quantized date to month  1995-05-01T00:00:00
Quantized date to week  1995-05-15T00:00:00
```
The following example executes action in each person nodes of the graph.

**Example 2:**
```jac
node person {
    has name;
    has birthday;
}

walker init {
    can date.quantize_to_year;

    root {
        person1 = spawn here ++> node::person(name="Josh", birthday="1995-05-20");
        person2 = spawn here ++> node::person(name="Joe", birthday="1998-04-23");
        person3 = spawn here ++> node::person(name="Jack", birthday="1997-03-12");
        take -->;
    }

    person {
        birthyear = date.quantize_to_year(here.birthday);
        std.out(here.name," Birthdate Quantized to year ",birthyear);
        }
}
```

**Output 2:**
```
Josh  Birthdate Quantized to year  1995-01-01T00:00:00
Joe  Birthdate Quantized to year  1998-01-01T00:00:00
Jack  Birthdate Quantized to year  1997-01-01T00:00:00
```

## Basic actions with presets and event triggers


> **Note**
> `here` refers to the current node scope pertinent to the program's execution point and `visitor` refers to the pertinent walker scope pertinent to that particular point of execution. All variables, built-in characteristics, and operations of the linked object instance are fully accessible through these references.
>

**Example 3:**
```
node person {
    has name;
    has byear;

    #this sets the birth year from the setter
    can date.quantize_to_year::visitor.year::>byear with setter entry;

    #this executes upon exit of the walker from node
    can std.out::byear," from ", visitor.info:: with exit;

}

walker init {

    #collect the current time
    has year=std.time_now();
    root {
        person1 = spawn here ++> node::person(name="Josh", byear="1992-01-01");
        take --> ;
    }

    person {
        spawn here walker::setter;
    }
}

walker setter {
    has year="1995-01-01";
    }
```

**Output 3:**
```
1995-01-01T00:00:00  from  {"name": "setter", "kind": "walker", "jid": "urn:uuid:a3e5f4b6-aeda-4cd0-9552-506cb3b7c693", "j_timestamp": "2022-11-09T09:10:05.134836", "j_type": "walker", "context": {"year": "1995-01-01"}}
1995-01-01T00:00:00  from  {"name": "init", "kind": "walker", "jid": "urn:uuid:47f1e467-a0e6-4772-a06a-204f6a1b69c3", "j_timestamp": "2022-11-09T09:10:05.129720", "j_type": "walker", "context": {"year": "2022-11-09T09:10:05.131397"}}
```