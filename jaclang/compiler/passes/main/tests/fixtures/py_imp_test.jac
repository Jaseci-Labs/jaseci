import:py math;
import:py argparse;
import:py from pygame_mock { color }
import:py pygame_mock;
import:py os;

with entry {
    b = math.floor(1.7);
    c: color.Color = color.Color(pygame_mock.constants.CONST_VALUE);
    c2: pygame_mock.color.Color = color.Color(pygame_mock.constants.CL.CONST_VALUE2);
    a: argparse.ArgumentParser = argparse.ArgumentParser();
    print("Hello", 1, b);
    pygame_mock.display.set_mode(WIN_WIDTH, WIN_HEIGHT);
    print(os.path.isfile("/jj"));
}
