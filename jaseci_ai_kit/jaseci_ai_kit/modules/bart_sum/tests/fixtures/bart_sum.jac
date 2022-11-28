walker test_summarize_single {
    can bart_sum.summarize;
    report bart_sum.summarize("There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.", 10);
}

walker test_summarize_url {
    can bart_sum.summarize;
    report bart_sum.summarize(null, "https://in.mashable.com/");
}

walker test_summarize_batch {
    can bart_sum.summarize;
    report bart_sum.summarize(
        ["There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.", 
        "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.",
        "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude."], 
        10
    );
}