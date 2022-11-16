walker summarize {
	has iters = 1;
	can cl_summer.summarize;
	root {
		durs = [];
		for i=0 to i<iters by i+=1 {
			x = "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.";
			x += " The King of England was at war with him and had led a great army into Scotland to drive him out of the land.";
			x += "Battle after battle had been fought. Six times Bruce had led his brave little army against his foes and six times his men had been beaten and driven into flight.";
			x += "At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains. ";
			x += "One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him. He was tired and unhappy.";
			x += " He was ready to give up all hope. It seemed to him that there was no use for him to try to do anything more. As he lay thinking, he saw a spider over his head making ready to weave her web. ";
			x += "He watched her as she toiled slowly and with great care. Six times she tried to throw her frail thread from one beam to another, and six times it fell short. 'Poor thing,' said Bruce: 'you, too, know what it is to fail.'";
			x += " But the spider did not lose hope with the sixth failure. With still more care, she made ready to try for the seventh time. Bruce almost forgot his own troubles as he watched her swing herself out upon the slender line.";
			x += " Would she fail again? No! The thread was carried safely to the beam and fastened there.";

			start_time = std.time_now();
			cl_summer.summarize(text=x, url="none", sent_count=5, summarizer_type="LsaSummarizer");
			end_time = std.time_now();
			durs = durs + [ [ start_time, end_time ] ];
		}
		report durs;
	}
}