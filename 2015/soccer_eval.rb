#!/usr/bin/ruby

teams=Hash.new{|h,k|h[k]=[]}

File.open('2015_J1_1st_final_game.csv',:encoding=>Encoding::Windows_31J){|f|
	f.gets
	while line=f.gets
		a=line.chomp.split(',')
		teams[a[4].to_i]<<[a[7].to_i,a[10].to_i]
		teams[a[7].to_i]<<[a[4].to_i,a[11].to_i]
	end
}
n=0
s=0.0
f=ARGF
	while line=f.gets
		a=line.split(',')
		team=a[0].to_i
		score=a[1].to_f
		s+=(teams[team][0][1]-score)**2
		n+=1
	end
#}
p Math.sqrt(s/n)