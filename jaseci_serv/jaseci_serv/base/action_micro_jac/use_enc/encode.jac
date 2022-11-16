walker encode {
	has iters = 1;
	can use.encode;
	root {
		durs = [];
		for i=0 to i<iters by i+=1 {
			start_time = std.time_now();
			use.encode("Some texts here!");
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}