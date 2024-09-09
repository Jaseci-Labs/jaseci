node state {
    has name = rand.word();
    has response="I'm a silly bot.";
    has user_utter;

    can speak with entry {
        std.out(response + " I'm current on "+name+" node");
    }

    can listen with talker exit {
        user_utter = visitor.utterance;
        visitor.path.l::append(&here);
        std.out("I heard "+user_utter+".");
    }

    can test_path with get_states entry {
        visitor.path.l::append(&here);
    }
}

node hop_state {
    has name;
    can log with exit {
        std.log("A walker is walking right over me.");
    }
}