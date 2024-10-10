import from enum { unique }

@unique
enum Color;

:enum:Color {
    RED = 1,
    GREEN = 2
}

enum :protect Role {
    ADMIN = 'admin',
    USER = 'user',
    with entry {
        print('Initializing role system..');
    },
    can foo -> str {
        return 'Accessing privileged Data';
    }
}
with entry {
    print(Color.RED.value, Role.foo());
}
