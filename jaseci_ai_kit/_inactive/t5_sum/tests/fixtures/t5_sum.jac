walker test_t5_sum_detection{
    can t5_sum.classify_text;
    text = "The US has passed the peak on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month.";
    report t5_sum.classify_text(text=text,min_length=30,max_length=100);
}
