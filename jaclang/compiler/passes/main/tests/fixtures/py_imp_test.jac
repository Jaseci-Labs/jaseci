import:py math;
import:py argparse;
import:py from pygame, color;
import:py pygame;
import:py os;

with entry {
    b = math.floor(1.7);
    c: color.Color = color.Color(pygame.AUDIO_ALLOW_ANY_CHANGE);
    c2: pygame.color.Color = color.Color(pygame.AUDIO_ALLOW_ANY_CHANGE);
    a: argparse.ArgumentParser = argparse.ArgumentParser();
    print("Hello", 1, b + int(c));
    pygame.display.set_mode(WIN_WIDTH, WIN_HEIGHT);
    print(os.path.isfile("/jj"));
}
