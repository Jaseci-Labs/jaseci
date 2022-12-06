walker test_valid_pdf_url {
    can pdf_ext.extract_pdf;
    report pdf_ext.extract_pdf("http://www.africau.edu/images/default/sample.pdf", "", false);
}

walker test_metadata_enabled {
    can pdf_ext.extract_pdf;
    report pdf_ext.extract_pdf("http://www.africau.edu/images/default/sample.pdf", "", true);
}

walker test_metadata_disabled {
    can pdf_ext.extract_pdf;
    report pdf_ext.extract_pdf("http://www.africau.edu/images/default/sample.pdf", "", false);
}