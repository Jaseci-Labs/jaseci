import:py pygame;

obj Spritesheet {
    can init(file: str);
    can get_sprite(x: int, y: int, width: int, height: int) -> pygame.Surface;
}

:obj:Spritesheet:can:init
(file: str) {
    self.sheet = pygame.image.load(file).convert();
}

:obj:Spritesheet:can:get_sprite
(x: int, y: int, width: int, height: int) {
    sprite = pygame.Surface([width, height]);
    sprite.blit(self.sheet, (0, 0), (x, y, width, height));
    sprite.set_colorkey(BLACK);
    return sprite;
}
