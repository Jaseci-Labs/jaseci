import:py from jaclang.runtimelib.architype {Anchor}
import:py from uuid {UUID}

node A {
    has val: int;
}

walker check_node {
    can enter with `root entry {
        visit [-->];
    }

    can enter2 with A entry {
        print(here);
    }
}

walker update_node {
    has val: int;

    can enter2 with A entry {
        here.val = self.val;
    }
}

walker create_node {
    has val: int;

    can enter with `root entry {
        a = A(val=self.val);
        here ++> a;
        print(a.__jac__.id);
    }
}

walker create_other_root {
    can enter with `root entry {
        other_root = `root().__jac__;
        other_root.save();
        print(other_root.id);
    }
}

walker allow_other_root_access {
    has root_id: str, level: int | str = 1, via_all: bool = False;

    can enter_root with `root entry {
        if self.via_all {
            here.__jac__.unrestrict(self.level);
        } else {
            here.__jac__.allow_root(UUID(self.root_id), self.level);
        }
    }

    can enter_nested with A entry {
        if self.via_all {
            here.__jac__.unrestrict(self.level);
        } else {
            here.__jac__.allow_root(UUID(self.root_id), self.level);
        }
    }
}

walker disallow_other_root_access {
    has root_id: str, via_all: bool = False;

    can enter_root with `root entry {
        if self.via_all {
            here.__jac__.restrict();
        } else {
            here.__jac__.disallow_root(UUID(self.root_id));
        }
    }

    can enter_nested with A entry {
        if self.via_all {
            here.__jac__.restrict();
        } else {
            here.__jac__.disallow_root(UUID(self.root_id));
        }
    }
}