walker test_topic_ext{
    can topic_ext.topic_extraction;
    has texts = ["still waiting card",
        "countries supporting",
        "card still arrived weeks",
        "countries accounts suppor",
        "provide support countries",
        "waiting week card still coming",
        "track card process delivery",
        "countries getting support",
        "know get card lost",
        "send new card",
        "still received new card",
        "info card delivery",
        "new card still come",
        "way track delivery card",
        "countries currently support"
        ];
    has labels = [2, 0, 2, 0, 0, 2, 1, 0, 2, 3, 3, 1, 3, 1, 0];

    report topic_ext.topic_extraction(texts=texts,classes=labels,n_topics=5,min_tokens=1,max_tokens=2);
}


walker test_headline_gen{
    can topic_ext.headline_generation;
    has texts = ["still waiting card",
        "countries supporting",
        "card still arrived weeks",
        "countries accounts suppor",
        "provide support countries",
        "waiting week card still coming",
        "track card process delivery",
        "countries getting support",
        "know get card lost",
        "send new card",
        "still received new card",
        "info card delivery",
        "new card still come",
        "way track delivery card",
        "countries currently support"
        ];
    has labels = [2, 0, 2, 0, 0, 2, 1, 0, 2, 3, 3, 1, 3, 1, 0];

    report topic_ext.headline_generation(texts=texts,classes=labels);
}

walker test_keyword_ext{
    can topic_ext.keyword_extraction;
    has texts = "I like dogs";

    report topic_ext.keyword_extraction(sentence=texts, n_words=2, min_tokens = 1, max_tokens = 1, diversity = 0.02);
}