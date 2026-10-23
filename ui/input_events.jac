"""Host-event value objects shared by the input decoder and normalizer."""


glob ESC: str = "\x1b";
glob BRACKETED_PASTE_START: str = "\x1b[200~";
glob BRACKETED_PASTE_END: str = "\x1b[201~";


obj HostEvent {
    has kind: str = "";
}


obj TextEvent(HostEvent) {
    has text: str = "";

    def init(text: str = "") {
        self.kind = "text";
        self.text = text;
    }
}


obj KeyEvent(HostEvent) {
    has key: str = "";

    def init(key: str = "") {
        self.kind = "key";
        self.key = key;
    }
}


obj PasteEvent(HostEvent) {
    has text: str = "";

    def init(text: str = "") {
        self.kind = "paste";
        self.text = text;
    }
}


obj ResizeEvent(HostEvent) {
    has width: int = 0,
        height: int = 0;

    def init(width: int = 0, height: int = 0) {
        self.kind = "resize";
        self.width = width;
        self.height = height;
    }
}


obj MouseEvent(HostEvent) {
    has button: int = 0,
        x: int = 0,
        y: int = 0,
        pressed: bool = False,
        motion: bool = False;

    def init(
        button: int = 0,
        x: int = 0,
        y: int = 0,
        pressed: bool = False,
        motion: bool = False,
    ) {
        self.kind = "mouse";
        self.button = button;
        self.x = x;
        self.y = y;
        self.pressed = pressed;
        self.motion = motion;
    }
}


obj StreamChunkEvent(HostEvent) {
    has text: str = "";

    def init(text: str = "") {
        self.kind = "stream";
        self.text = text;
    }
}

obj EofEvent(HostEvent) {
    def init() {
        self.kind = "eof";
    }
}


obj InterruptEvent(HostEvent) {
    def init() {
        self.kind = "interrupt";
    }
}
