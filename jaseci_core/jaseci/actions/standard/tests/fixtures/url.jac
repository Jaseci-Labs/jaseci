walker is_valid_test {
    report url.is_valid('https://www.jaseci.org');
    report url.is_valid('www.jaseci.org');
    report url.is_valid('www.jaseki.org');
}

walker ping_test {
    report url.ping('https://www.jaseci.org');
    report url.ping('www.jaseci.org');
    report url.ping('https://www.jasec1.org');
    report url.ping('https://www.jaseci.com');
}

walker download_text_test {
    report url.download_text('https://www.jaseci.org');
}

walker download_b64_test {
    report url.download_b64('https://www.jaseci.org/wp-content/uploads/2022/06/2206.08434.pdf');
}
