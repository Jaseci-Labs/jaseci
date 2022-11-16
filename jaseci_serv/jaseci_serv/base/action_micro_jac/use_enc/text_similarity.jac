walker text_similarity {
	has iters = 1;
	can use.text_similarity;
	root {
		durs = [];
		for i=0 to i<iters by i+=1 {
			start_time = std.time_now();
			use.text_similarity("This is the first string", "This is the second string");
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}