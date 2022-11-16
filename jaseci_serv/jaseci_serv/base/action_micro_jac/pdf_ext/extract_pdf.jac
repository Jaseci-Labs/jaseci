walker extract_pdf {
	has iters = 1;
	can pdf_ext.extract_pdf;
	root {
		for i=0 to i<iters by i+=1 {
			pdf_ext.extract_pdf("http://www.africau.edu/images/default/sample.pdf", true);
		}
	}
}