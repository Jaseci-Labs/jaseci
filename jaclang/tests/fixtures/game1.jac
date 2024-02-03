import:py pygame;

import:py from typing, Tuple;

obj Button{
    can is_pressed(pos: tuple, pressed:str) -> bool {
        return True;
    }
}

can ttt() -> int {
    b = Button();
    a = pygame.mouse.get_pressed();
    b.is_pressed((1, 2, 3), a);
    return 0;
}


