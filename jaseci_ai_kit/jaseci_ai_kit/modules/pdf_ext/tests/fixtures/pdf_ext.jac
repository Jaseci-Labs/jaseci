walker test_valid_pdf_url {
    can pdf_ext.extract_pdf;
    report pdf_ext.extract_pdf(url="http://www.africau.edu/images/default/sample.pdf", metadata=false);
}

walker test_metadata_enabled {
    can pdf_ext.extract_pdf;
    report pdf_ext.extract_pdf(url="http://www.africau.edu/images/default/sample.pdf", metadata=true);
}

walker test_metadata_disabled {
    can pdf_ext.extract_pdf;
    report pdf_ext.extract_pdf(url="http://www.africau.edu/images/default/sample.pdf", metadata=false);
}