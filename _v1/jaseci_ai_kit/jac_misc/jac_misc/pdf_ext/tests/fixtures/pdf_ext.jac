walker test_valid_pdf_url {
    can pdf_ext.extract_pdf;
    report pdf_ext.extract_pdf(url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", metadata=false);
}

walker test_metadata_enabled {
    can pdf_ext.extract_pdf;
    report pdf_ext.extract_pdf(url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", metadata=true);
}

walker test_metadata_disabled {
    can pdf_ext.extract_pdf;

    report pdf_ext.extract_pdf(url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", metadata=false);
}