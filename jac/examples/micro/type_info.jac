import pygame;

obj Spritesheet {
    def init(file: str);
    def get_sprite(x: int, y: int, width: int, height: int) -> pygame.Surface;
}

impl def Spritesheet.init
(file: str) {
    self.sheet = pygame.image.load(file).convert();
}

impl def Spritesheet.get_sprite
(x: int, y: int, width: int, height: int) {
    sprite = pygame.Surface([width, height]);
    sprite.blit(self.sheet, (0, 0), (x, y, width, height));
    sprite.set_colorkey(BLACK);
    return sprite;
}
