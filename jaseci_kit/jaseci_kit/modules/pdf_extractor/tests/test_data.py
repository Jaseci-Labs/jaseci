# flake8: noqa
test_valid_pdf_url_payload = {
    "url": "http://www.africau.edu/images/default/sample.pdf",
    "metadata": False,
}
test_invalid_pdf_url_payload = {
    "url": "https://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_480_1_5MG.mp4",
    "metadata": True,
}

test_metadata_enabled_payload = {
    "url": "http://www.africau.edu/images/default/sample.pdf",
    "metadata": True,
}

test_metadata_disabled_payload = {
    "url": "http://www.africau.edu/images/default/sample.pdf",
    "metadata": False,
}
