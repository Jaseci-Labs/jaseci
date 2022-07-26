node state {
    has name = rand.word().str::upper;
    has response = "I'm a silly bot. ";
    has user_utter;

    can speak with entry {
        std.out("I'm "+name+". And I currently have " + visitor.info['name'] +
                " on me! ");
    }

    can listen with talker exit {
        user_utter = visitor.utterance;
        std.out("I heard '"+user_utter+"'\n");
        std.out(response);
    }

    can test_path with hop_counter entry {
        visitor.path.l::append(&here);
    }
}

walker init {
    root {
        n1 = spawn here --> node::state;
        n2 = spawn here --> node::state;
    }
    spawn here walker::talker;
    spawn here walker::hop_counter;
}

walker talker {
    has utterance, path = [];
    utterance = rand.sentence();
    take -->;
}

walker hop_counter {
    has anchor path = [];
    take -->;

    with exit { std.out("\nHopper's path:", path); }
}
