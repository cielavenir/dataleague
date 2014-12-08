#!/usr/bin/ruby
#coding:utf-8

#baseball eval
#I have trashed the data, so this program is not verified...

class Array
	def sum() self.reduce(0,:+) end
	def average() sum/size end
end
		
def dcg(a)
	return 0 if a.empty?
	if false
		a[0]+2.step(a.size).map{|i|a[i-1]/Math.log2(i)}.sum
	else
		1.step(a.size).map{|i|(2**a[i-1]-1)/Math.log2(i+1)}.sum
	end
end

def parse(s)
	#h[category][順位]=選手ID
	h=Hash.new{|h,k|h[k]=Hash.new(0)}
	File.open(s){|f|
		while line=f.gets
			a,c=line.chomp.split(',')
			a,b=a.split('_')
			h[a][b.to_i]=c
		end
	}
	h
end

TARGET_YEAR=2013
positions=['MVP','投手','捕手','一塁手','二塁手','三塁手','遊撃手','左翼手','中堅手','右翼手','指名打者','外野手']

if ARGV.empty?
	puts 'baseball_eval.rb submission.csv'
	exit
end

#data[category][選手ID]=占有率
data=Hash.new{|h,k|h[k]=Hash.new(0)}
File.open('mvp_test.csv',:encoding=>Encoding::Windows_31J){|f|
	f.gets
	while line=f.gets
		a=line.chomp.split(',')
		if a[0].to_i==TARGET_YEAR
			data[a[2]+'-0'][a[1]]=a[9].to_f
		end
	end
}
File.open('best_nine_test.csv',:encoding=>Encoding::Windows_31J){|f|
	f.gets
	while line=f.gets
		a=line.chomp.split(',')
		if a[0].to_i==TARGET_YEAR
			data[a[1]+'-'+positions.index(a[5]).to_s][a[1]]=a[7].to_f
		end
	end
}
input=parse(ARGV[0])
p input.map{|k,v|
	idcg=dcg(data[k].values.sort.reverse[0,20])
	d=dcg((1..20).map{|e|data[k][ v[e] ]})
	d/idcg
}.average