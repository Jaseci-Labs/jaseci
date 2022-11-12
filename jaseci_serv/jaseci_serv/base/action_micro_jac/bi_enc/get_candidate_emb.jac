walker get_candidate_emb {
	can bi_enc.get_candidate_emb;
	root {
		durs = [];
		for i=0 to i<100 by i+=1 {
			start_time = std.time_now();
			bi_enc.get_candidate_emb(["Hello"]);
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}