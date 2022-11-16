walker infer {
	has iters = 1;
	can bi_enc.infer;
	root {
		durs = [];
		for i=0 to i<iters by i+=1 {
			start_time = std.time_now();
			bi_enc.infer(["Hello"], ["Hello", "GoodBye"], "text", "text");
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}