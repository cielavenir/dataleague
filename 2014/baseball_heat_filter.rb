#!/usr/bin/ruby

#Now, baseball_learn.py should be used directly.
players={}
File.open('submission_sample.csv'){|f|
	while line=f.gets
		a=line.split('_')
		players[a[0].to_i]=1
	end
}
File.open('train.csv'){|f|
	f.gets
	while line=f.gets
		a=line.chomp.split(',')
		if players.has_key?(a[3].to_i)
			puts line.gsub('NA','0')
		end
	end
}