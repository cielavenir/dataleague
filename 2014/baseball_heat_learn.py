#!/usr/bin/python
#coding:utf-8

#https://careeful.com/contestDetails/?ci=S004
#https://crowdsolving.jp/node/1099/

import sys,itertools
from collections import defaultdict
from sklearn.linear_model import LinearRegression
if sys.version_info[0]>=3: raw_input=input

data=[]
f=open('submission_sample.csv')
try:
	while True:
		line=f.readline().rstrip()
		if not line: break
		a=line.split(',')[0].split('_')
		data.append((int(a[0]),int(a[1])*12+int(a[2])-1))
except EOFError:
	pass
f.close()

players=defaultdict(dict)
f=open('train.csv')
try:
	f.readline() # drop header
	while True:
		line=f.readline().rstrip().replace('NA','0')
		if not line: break
		a=line.split(',')
		player_id=int(a[3])
		year=int(a[0])
		month=int(a[4])
		total_month=year*12+month-1
		if 'factor' not in players[player_id]: players[player_id]['factor']=[]
		#G(打席)-Q(四球)
		players[player_id]['factor'].append(
			[total_month]+
			list(itertools.chain.from_iterable((int(e),int(e)**2) for e in a[6:16+1]))
		)
		if 'train' not in players[player_id]: players[player_id]['train']=[]
		players[player_id]['train'].append(float(a[-1]))
except EOFError:
	pass
f.close()

for player,month in data:
	if player in players:
		clf = LinearRegression()
		clf.fit(players[player]['factor'],players[player]['train'])
		lastmonth=players[player]['factor'][-1][0]
		rate=players[player]['train'][-1]
		newrate=rate+clf.coef_[0]*(month-lastmonth)
		if newrate<0: newrate=0
		print('%d_%d_%d,%.9f'%(player,month//12,month%12+1,newrate))
	else:
		print('%d_%d_%d,0.2'%(player,month//12,month%12+1)) # データが1件もない選手は0.2に固定…。