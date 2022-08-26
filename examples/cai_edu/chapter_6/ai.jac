node ai_model {
    can train with train entry {}
    can test_model with test_model entry {}
    can eval with eval entry {
        ::train;
        ::test_model;
    }
    can infer with infer entry {}
}

walker train {
    has train_file, num_train_epochs, from_scratch;
    has batch_size, learning_rate;
}

walker test_model {
    has eval_file;
}

walker eval {
    has train_file, eval_file, num_train_epochs, from_scratch;
}

walker infer {
    has input;
}