import os;

node Room {
    has name: str;
}

walker Tour {
    has seen: list[str] = [];

    can start with Root entry {
        visit [-->];
    }

    can at_room with Room entry {
        self.seen.append(here.name);
        visit [-->];
    }
}

def env_flag(name: str) -> bool {
    return os.environ.get(name, "") == "1";
}

with entry {
    root ++> Room(name="a") ++> Room(name="b");
    print((root spawn Tour()).seen, env_flag("PARITY_UNSET"));
}
