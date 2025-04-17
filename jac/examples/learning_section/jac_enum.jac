enum Color {
    RED,
    GREEN,
    BLUE
}

with entry {
    print(Color.RED);
}

enum Status {
    SUCCESS = 1,
    FAILURE = 0
}

with entry {
    print(Status.SUCCESS.value);
}

import from enum { unique }

@unique
enum Color {
    RED = 1,
    GREEN = 2
}

with entry {
    print(Color.RED.value);
}

enum :protect Role {
    ADMIN = 'admin',
    USER = 'user'
}

with entry {
    print(Role.ADMIN.value);
}

enum Role {
    ADMIN = 'admin',
    USER = 'user',
    can get_permissions(role: Role) -> str {
        return 'Full Access' if role == Role.ADMIN else 'Limited Access';
    }
}

with entry {
    print(Role.ADMIN.get_permissions());
}

enum Status {
    ACTIVE = 1,
    INACTIVE = 0,
    with entry {
        print("Initializing Status Enum...");
    }
}

with entry {
    print(Status.ACTIVE.value);
}

obj Vehicle {
    has brand: str;

    enum Type {
        CAR,
        BIKE,
        TRUCK
    }
}

with entry {
    print(Vehicle.Type.CAR.value);
}

obj Outer {
    has o1: int = 9;

    obj Inner {
        has i1: int = 8;
    }
    enum Color {
        RED,
        GREEN,
        BLUE,
        with entry {
            print("Initializing Color Enum...");
        },
        can describe -> str {
            return "This is a color enum";
        }
    }
}

with entry {
    print(Outer.Color.GREEN.value, Outer.Color.describe());
}

with entry {
    if Role.ADMIN == Role.USER {
        print("Same role");
    } else {
        print("Different roles");
    }
}

with entry {
    for role in Role {
        print(role, role.value);
    }
}
