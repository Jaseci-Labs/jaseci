import:py random;
import:py from typing, Tuple;

obj Button {
    can is_pressed(pos: tuple, pressed: str) -> bool {
        return True;
    }
}

can ttt() -> int {
    b = Button();
    a = random.randint(1, 10);
    b.is_pressed((1, 2, 3), a);
    return 0;
}
