walker answer_similarity {
	has iters = 1;
	can use.answer_similarity;
	root {
		durs = [];
		for i=0 to i<iters by i+=1 {
			start_time = std.time_now();
			use.answer_similarity("Am I JACK?", "Am I Jack?");
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}