import from typing { Final }

obj Once {
    has x: Final[int],
        tag: Final[str] postinit;

    def init(v: int) {
        self.x = v;
    }

    def postinit {
        self.tag = "t";
    }
}

obj Branches {
    has x: Final[int];

    def init(flag: bool) {
        if flag {
            self.x = 1;
        } else {
            self.x = 2;
        }
    }
}

obj Deferred {
    has x: Final[int],
        tag: Final[str] postinit;

    def postinit {
        self.tag = "t";
    }
}

obj Twice {
    has x: Final[int];

    def init(v: int) {
        self.x = v;
        self.x = v + 1;  # <-- Error
    }
}

obj InitThenPost {
    has x: Final[int];

    def init(v: int) {
        self.x = v;
    }

    def postinit {
        self.x = 99;  # <-- Error
    }
}

obj InLoop {
    has x: Final[int];

    def init(vs: list[int]) {
        for v in vs {
            self.x = v;  # <-- Error
        }
    }
}

obj PassedThenPost {
    has x: Final[int];

    def postinit {
        self.x = 99;  # <-- Error
    }
}
