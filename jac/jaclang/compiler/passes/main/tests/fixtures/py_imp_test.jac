import:py math;
import:py argparse;
import:py from pygame_mock { color, display }
import:py pygame_mock;
import:py os;

can fool_me -> `Type[pygame_mock.constants.CL] {
    return pygame_mock.constants.CL;
}

obj kk {
    can fool_me -> `Type[pygame_mock.constants.CL] {
        return pygame_mock.constants.CL;
    }
}

with entry {
    b = math.floor(1.7);
    c: color.Color = color.Color(pygame_mock.constants.CONST_VALUE);
    c2: pygame_mock.color.Color = color.Color(pygame_mock.constants.CL.CONST_VALUE2);
    c3: pygame_mock.color.Color = color.Color(fool_me().CONST_VALUE2);
    c4: pygame_mock.color.Color = color.Color(kk().fool_me().CONST_VALUE2);
    g = fool_me();
    c4: pygame_mock.color.Color = color.Color(g.CONST_VALUE2);
    a: argparse.ArgumentParser = argparse.ArgumentParser();
    print("Hello", 1, b);
    pygame_mock.display.set_mode(WIN_WIDTH, WIN_HEIGHT);
    print(os.path.isfile("/jj"));
}
