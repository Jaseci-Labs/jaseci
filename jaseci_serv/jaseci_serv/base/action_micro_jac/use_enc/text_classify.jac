walker text_classify {
	has iters = 1;
	can use.text_classify;
	root {
		durs = [];
		for i=0 to i<iters by i+=1 {
			start_time = std.time_now();
			use.text_classify("Classify this string", ["Class 1", "Class 2"]);
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}