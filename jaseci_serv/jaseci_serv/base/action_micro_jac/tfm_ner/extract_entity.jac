walker extract_entity {
	can tfm_ner.extract_entity;
	root {
		durs = [];
		for i=0 to i<100 by i+=1 {
			start_time = std.time_now();
			tfm_ner.extract_entity("The Humboldt University of Berlin is situated in Berlin, Germany");
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}