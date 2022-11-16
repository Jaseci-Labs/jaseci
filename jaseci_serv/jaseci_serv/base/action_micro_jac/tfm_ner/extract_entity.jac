walker extract_entity {
	has iters = 1;
	can tfm_ner.extract_entity;
	root {
		for i=0 to i<iters by i+=1 {
			res = tfm_ner.extract_entity("The Humboldt University of Berlin is situated in Berlin, Germany");
		}
		report res;
	}
}