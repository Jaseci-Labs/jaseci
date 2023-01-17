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

    report topic_ext.topic_extraction(texts=texts,classes=labels,n_topics=5);
}