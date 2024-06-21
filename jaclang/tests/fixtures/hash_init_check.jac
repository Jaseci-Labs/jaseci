obj TYPE {
    can init() {
        DICT:dict = {};
        DICT[self] = 1;
    }
}

obj TASK:TYPE: {
    can init() {
        TYPE.init(self);
    }
}

with entry {
    TASK();
    print('Test Passed');
}