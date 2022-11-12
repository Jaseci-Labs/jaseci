walker extract_pdf {
	can pdf_ext.extract_pdf;
	root {
		for i=0 to i<100 by i+=1 {
			pdf_ext.extract_pdf("http://www.africau.edu/images/default/sample.pdf", true);
		}
	}
}