walker entity_detection {
	has iters = 1;
	can ent_ext.entity_detection;
	root {
		durs = [];
		for i=0 to i<iters by i+=1 {
			start_time = std.time_now();
			ent_ext.entity_detection("The Humboldt University of Berlin is situated in Berlin, Germany", ["LOC", "ORG"]);
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}