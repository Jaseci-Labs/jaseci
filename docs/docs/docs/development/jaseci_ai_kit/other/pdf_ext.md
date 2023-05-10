---
sidebar_position: 3
title: PDF Extractor Module
description: Detect topical changes in Documents.
---

# PDF Extractor Module

`pdf_ext` module implemented for the Topical Change Detection in Documents via Embeddings of Long Sequences.

### Actions

* `extract_pdf`: gets different topics in the context provided, given a threshold
    * Input
        * `url`(String): gets the pdf from URL
        * `path`(Float): gets the pdf from local path
        * `metadata`(Bool): to display available metadata of PDF
    * Returns: a json with number of pages the pdf had and content

### Example Jac Usage

```jac
walker pdf_ext_example {
    has url = "http://www.africau.edu/images/default/sample.pdf";
    has metadata = true;
    can pdf_ext.extract_pdf;

    # Getting the dat from PDF
    resp_data = pdf_ext.extract_pdf(url=url,
    metadata=metadata);
    std.out(resp_data);
}
```

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/pdf_ext)