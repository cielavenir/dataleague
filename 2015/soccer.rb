#!/usr/bin/ruby
class Array
	def average1
		a=self
		a.reduce(:+).to_f/a.size
	end
	def average2
		a=self.sort[1...-1]
		a.reduce(:+).to_f/a.size
	end
	def median
		a=self.sort
		n=a.size
		(a[n/2]+a[~-n/2])/2
	end

	# --- #

	def average
		average1
		#(average1+average2)/2
	end
end

teams=Hash.new{|h,k|h[k]=Hash.new{|h1,k1|h1[k1]=[]}}
final_game={}

File.open('2015_J1_1st-2nd_Result.csv',:encoding=>Encoding::Windows_31J){|f|
	f.gets
	while line=f.gets
		a=line.chomp.split(',')
		teams[a[4].to_i][a[7].to_i]<<a[10].to_i
		teams[a[7].to_i][a[4].to_i]<<a[11].to_i
	end
}
=begin
File.open('2015_J1_2nd_final_game.csv',:encoding=>Encoding::Windows_31J){|f|
	f.gets
	while line=f.gets
		a=line.chomp.split(',')
		final_game[a[4].to_i]=a[7].to_i
		final_game[a[7].to_i]=a[4].to_i
	end
}
=end
File.open('submission_sample_0.csv'){|f|
	while line=f.gets
		a=line.split(',')
		team=a[0].to_i
		s=0
		n=0
		teams[team].each{|opponent,score|
			s+=score.average;n+=1
			#score.each{|e|
			#	s+=e;n+=1
			#}
		}
		puts '%d,%f'%[team,s/n]
	end
}