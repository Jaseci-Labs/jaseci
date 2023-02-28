walker test_summarize_single {
    can bart_sum.summarize;
    report bart_sum.summarize(text="There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.", min_length=10);
}

walker test_summarize_single_percentage {
    can bart_sum.summarize;
    report bart_sum.summarize(text="There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.", min_length=0.2, max_length=0.5);
}

walker test_summarize_url {
    can bart_sum.summarize;
    report bart_sum.summarize(url="https://in.mashable.com/");
}

walker test_summarize_batch {
    can bart_sum.summarize;
    report bart_sum.summarize(
        ["There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.",
        "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.",
        "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude."]
    );
}