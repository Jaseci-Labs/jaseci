"""This is a RPG game built using Jaclang"""

# Import python modules
import:py pygame;
import:py sys;

# Importing Jac codebase
include:jac Sprites;
include:jac Config;
include:jac Map;

obj Game {
    can <init>(){
        pygame.init();

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT));
        self.clock = pygame.time.Clock();
        self.font = pygame.font.Font('8bitoperator_jve.ttf', 32);
        self.running = True;
        self.won = False;

        self.character_spritesheet = Spritesheet('img/character.png');
        self.terrain_spritesheet = Spritesheet('img/terrain.png');
        self.enemy_spritesheet = Spritesheet('img/enemy.png');
        self.attack_spritesheet = Spritesheet('img/attack.png');
        self.intro_background = pygame.image.load('./img/introbackground.png');
        self.go_background = pygame.image.load('./img/gameover.png');
    }

    can createTilemap(){
        for (i, row) in enumerate(tilemap){
            for (j, column) in enumerate(row){
                Ground(self,j,i);
                if column == "B"{
                    Block(self,j,i);
                }
                if column == "E"{
                    Enemy(self,j,i);
                }
                if column == "P"{
                    self.player = Player(self,j,i);
                }
            }
        }
    }

    can new(){
        self.playing = True;
        self.won = False;

        self.all_sprites = pygame.sprite.LayeredUpdates();
        self.blocks = pygame.sprite.LayeredUpdates();
        self.enemies = pygame.sprite.LayeredUpdates();
        self.attacks = pygame.sprite.LayeredUpdates();

        self.createTilemap();
    }

    can events(){
        for events in pygame.event.get(){
            if events.type == pygame.QUIT{
                self.playing = False;
                self.running = False;
            }
            keys = pygame.key.get_pressed();

            if keys[pygame.K_SPACE] {
                if self.player.facing == 'up'{Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE);}
                if self.player.facing == 'down'{Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE);}
                if self.player.facing == 'right'{Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y);}
                if self.player.facing == 'left'{Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y);}
            }
        }

    }

    can update(){
        self.all_sprites.update();
    }

    can draw(){
        self.screen.fill(BLACK);
        self.all_sprites.draw(self.screen);
        self.clock.tick(FPS);
        pygame.display.update();
    }

    can main(){
        while self.playing {
            self.events();
            self.update();
            self.draw();
            if len(self.enemies.sprites()) == 0 {
                self.won = True;
                self.playing = False;
            }
        }

        if self.won == False{
            self.playing = False;
        }
    }

    can game_over(){
        text = self.font.render('GaMe OvEr', True, RED);
        text_rect = text.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2));

        restart_button = Button(10,WIN_HEIGHT-135, 120, 125, WHITE, BLACK, 'Restart', 32);

        for sprite in self.all_sprites{sprite.kill();}

        while self.running{
            for event in pygame.event.get(){
                if event.type == pygame.QUIT{
                    self.running = False;
                }
            }
            mouse_pos = pygame.mouse.get_pos();
            mouse_pressed = pygame.mouse.get_pressed();

            if restart_button.is_pressed(mouse_pos, mouse_pressed) {
                self.won = False;
                self.new();
                break;
            }

            self.screen.blit(self.go_background, (0,0));
            self.screen.blit(text, text_rect);
            self.screen.blit(restart_button.image, restart_button.rect)   ; 
            self.clock.tick(FPS);
            pygame.display.update();
        }
    }

    can intro_screen() {
        intro = True;

        title = self.font.render('Spud-nik : SOLO', True, BLUE);
        title_rect = title.get_rect(x=WIN_WIDTH/2-100,y=100);

        play_button = Button(WIN_WIDTH/2-50, 200, 100, 100, WHITE, BLACK, 'Play', 32);

        while intro {
            for event in pygame.event.get(){
                if event.type == pygame.QUIT{
                    intro = False;
                    self.running = False;
                }
            }
            mouse_pos = pygame.mouse.get_pos();
            mouse_pressed = pygame.mouse.get_pressed();

            if play_button.is_pressed(mouse_pos, mouse_pressed) {
                intro = False;
            }

            self.screen.blit(self.intro_background, (0,0));
            self.screen.blit(title, title_rect);
            self.screen.blit(play_button.image, play_button.rect);
            self.clock.tick(FPS);
            pygame.display.update();
        }
    }

    can game_won {
        text = self.font.render('YOU WON!', True, BLUE);
        text_rect = text.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2));

        restart_button = Button(10,WIN_HEIGHT-135, 120, 125, WHITE, BLACK, 'Restart', 32);

        for sprite in self.all_sprites{sprite.kill();}

        while self.running{
            for event in pygame.event.get(){
                if event.type == pygame.QUIT{
                    self.running = False;
                }
            }
            mouse_pos = pygame.mouse.get_pos();
            mouse_pressed = pygame.mouse.get_pressed();

            if restart_button.is_pressed(mouse_pos, mouse_pressed) {
                self.new();
                break;
            }

            self.screen.blit(self.intro_background, (0,0));
            self.screen.blit(text, text_rect);
            self.screen.blit(restart_button.image, restart_button.rect)   ; 
            self.clock.tick(FPS);
            pygame.display.update();
        }
    }
}

glob g = Game();
with entry {
    g.intro_screen();
    g.new();
    while g.running {
        g.main();
        if g.won == True{
            print(g.won);
            g.game_won();
        } else {
            print(g.won);
            g.game_over();
        }
    }   

    pygame.quit();
    sys.exit();
}
