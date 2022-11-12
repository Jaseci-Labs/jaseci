walker answer_classify {
	can use.answer_classify;
	root {
		durs = [];
		for i=0 to i<100 by i+=1 {
			start_time = std.time_now();
			use.answer_classify("classify me!", ["Class 1", "Class 2"]);
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}