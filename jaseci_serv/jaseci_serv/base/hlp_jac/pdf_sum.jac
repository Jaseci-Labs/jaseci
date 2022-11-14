walker pdf_summarization {
    can cl_summer.summarize;
    can pdf_ext.extract_pdf;

    has path = null;
    has pdf = null;
    has sentence_count = 10;
    has doc_type = "default";

    content = "";

    pdf_extract = pdf_ext.extract_pdf(url=pdf, path=path, metadata=false);

    for data in pdf_extract['content']:
        content = content + " " + data;

    if (doc_type == "technical") {
        sum_type = "LuhnSummarizer";
    } else {
        sum_type = "LsaSummarizer";
    }

    summarized_data = cl_summer.summarize(text=content, url="none", sent_count=sentence_count, summarizer_type=sum_type);

    report summarized_data;

}