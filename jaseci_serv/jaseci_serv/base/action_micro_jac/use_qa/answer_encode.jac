walker answer_encode {
	can use.answer_encode;
	root {
		durs = [];
		for i=0 to i<100 by i+=1 {
			start_time = std.time_now();
			use.answer_encode("I am Jac.", "I am not Jack");
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}