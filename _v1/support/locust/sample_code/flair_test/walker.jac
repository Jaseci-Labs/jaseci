walker init {
    can ent_ext.entity_detection;
    root {
        report ent_ext.entity_detection(text = "Hello, I am from the University of Michigan!", ner_labels = ["University", "detection", "US", "Jaseci"])['entities'];
    }
}
