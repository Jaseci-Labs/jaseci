walker test_summarizer_text {
    can cl_summer.summarize;
    report cl_summer.summarize("There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.", "none", 1, "LsaSummarizer");
}

walker test_summarizer_url {
    can cl_summer.summarize;
    report cl_summer.summarize("none", "https://in.mashable.com/", 5, "LsaSummarizer");
}