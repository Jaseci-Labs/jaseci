# Walker and Node ability trigger sequence
```
node Node {
    has val: str;

    can entry1 with entry {
        print(f"{self.val}-2");
    }

    can entry2 with Walker entry {
        print(f"{self.val}-3");
    }

    can exit1 with Walker exit {
        print(f"{self.val}-4");
    }

    can exit2 with exit {
        print(f"{self.val}-5");
    }
}

walker Walker {
    can entry1 with entry {
        print("walker entry");
    }

    can entry2 with `root entry {
        print("walker enter to root");
        visit [-->];
    }

    can entry3 with Node entry {
        print(f"{here.val}-1");
    }

    can exit1 with Node exit {
        print(f"{here.val}-6");
    }

    can exit2 with exit {
        print("walker exit");
    }
}

with entry{
    root ++> Node(val = "a");
    root ++> Node(val = "b");
    root ++> Node(val = "c");

    Walker() spawn root;
}
```
## Current triggering sequence (jaclang version >= 0.7.29)
> **walker generic entry** => \
> **walker typed entry** => \
> **node generic entry** => \
> **node typed entry** => \
> **node typed exit** => \
> **node generic exit** => \
> **back to walker typed exit** => \
> **walker generic exit**
```
walker entry
walker enter to root
a-1
a-2
a-3
a-4
a-5
a-6
b-1
b-2
b-3
b-4
b-5
b-6
c-1
c-2
c-3
c-4
c-5
c-6
walker exit
```
## For jaclang version <= 0.7.28
> **walker generic entry** => \
> **node entries (generic/typed)** => \
> **back to walker typed entry** => \
> **walker typed exit** => \
> **back to node exits (generic/typed)** => \
> **back to walker generic exit**
```
walker entry
walker enter to root
a-2
a-3
a-1
a-6
a-4
a-5
b-2
b-3
b-1
b-6
b-4
b-5
c-2
c-3
c-1
c-6
c-4
c-5
walker exit
```
