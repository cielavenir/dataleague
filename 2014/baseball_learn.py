#!/usr/bin/python
#coding:utf-8

#https://careeful.com/contestDetails/?ci=S004
#https://crowdsolving.jp/node/1436/

import codecs,itertools
from functools import partial
from collections import defaultdict
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

target_year=2014
players_target_year=[None,set(),set()]
positions=[u'MVP',u'投手',u'捕手',u'一塁手',u'二塁手',u'三塁手',u'遊撃手',u'左翼手',u'中堅手',u'右翼手',u'指名打者',u'外野手']

train=[]
#年度*リーグID,選手ID,位置ID,占有率
for e in ['mvp_train.csv','mvp_test.csv']:
	f=codecs.open(e,mode='r',encoding='Shift-JIS')
	#年度,選手ID,リーグID,チームID,1位投票数,2位投票数,3位投票数,MVP点数,年度リーグ総点数,占有率
	try:
		f.readline()
		while True:
			line=f.readline().rstrip()
			if not line: break
			a=line.split(',')
			train.append([int(a[0])*int(a[2]),int(a[1]),0,float(a[9])])
	except EOFError:
		pass
	f.close()

for e in ['best_nine_train.csv','best_nine_test.csv']:
	f=codecs.open(e,mode='r',encoding='Shift-JIS')
	#年度,リーグID,選手ID,得票数,チームID,守備位置,年度リーグ守備位置別総得票数,占有率
	try:
		f.readline()
		while True:
			line=f.readline().rstrip()
			if not line: break
			a=line.split(',')
			train.append([int(a[0])*int(a[1]),int(a[2]),positions.index(a[5]),float(a[7])])
	except EOFError:
		pass
	f.close()

batting_train_columns=[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
batting_train=defaultdict(partial(defaultdict,partial(defaultdict,int)))
#[年度*リーグID][打者ID][パラメータ]
def batting_get(y,id):
	x=batting_train[y][id]
	return list(itertools.chain.from_iterable((x[i],) for i in range(len(batting_train_columns))))

for e in ['batting.csv','batting_added.csv']:
	f=codecs.open(e,mode='r',encoding='Shift-JIS')
	#年度,リーグID,チームID,打者ID,月,試合,打席,打数,得点,安打,二塁打,三塁打,本塁打,塁打,打点,三振,四球,死球,犠打,犠飛,盗塁,盗塁死,併殺打,打率,長打率,出塁率,OPS
	try:
		f.readline()
		while True:
			line=f.readline().rstrip()
			if not line: break
			a=line.split(',')
			for i,e in enumerate(batting_train_columns):
				batting_train[int(a[0])*int(a[1])][int(a[3])][i]+=int(a[e])
			if int(a[0])==target_year: players_target_year[int(a[1])].add(int(a[3]))
	except EOFError:
		pass
	f.close()

pitching_train_columns=[6,7,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25]
pitching_train=defaultdict(partial(defaultdict,partial(defaultdict,int)))
#[年度*リーグID][投手ID][パラメータ]
def pitching_get(y,id):
	x=pitching_train[y][id]
	return list(itertools.chain.from_iterable((x[i],) for i in range(len(pitching_train_columns))))

for e in ['pitching.csv','pitching_added.csv']:
	f=codecs.open(e,mode='r',encoding='Shift-JIS')
	#年度,リーグID,チームID,投手ID,月,登板,先発,救援,勝利,敗北,セーブ,ホールド,完投,完封勝利,投球回,打者,打数,被安打,被本塁打,与四球,与死球,奪三振,暴投,ボーク,失点,自責点,防御率,奪三振率,与四球率,与四死球率,被本塁打率,K/BB,WHIP,勝率,被打率
	try:
		f.readline()
		while True:
			line=f.readline().rstrip()
			if not line: break
			a=line.split(',')
			for i,e in enumerate(pitching_train_columns):
				pitching_train[int(a[0])*int(a[1])][int(a[3])][i]+=int(a[e])
			if int(a[0])==target_year: players_target_year[int(a[1])].add(int(a[3]))
	except EOFError:
		pass
	f.close()

#todo: 「順位」はそのまま活かすのは難しい。どうする？
position_rank_train=defaultdict(partial(defaultdict,partial(defaultdict,int)))
#[年度*リーグID][投手ID][ポジション]
def position_rank_get(y,id,position):
	return [pitching_train[y][id][position]]

for e in ['position.csv','position_added.csv']:
	f=codecs.open(e,mode='r',encoding='Shift-JIS')
	#年度,リーグID,チームID,選手ID,位置ID,位置名,ポジション順位
	try:
		f.readline()
		while True:
			line=f.readline().rstrip()
			if not line: break
			a=line.split(',')
			position_rank_train[int(a[0])*int(a[1])][int(a[3])][11 if 7<=int(a[4])<=9 else int(a[4])]=max(
				200-10*int(a[6]),
				position_rank_train[int(a[0])*int(a[1])][int(a[3])][11 if 7<=int(a[4])<=9 else int(a[4])]
			)
			if int(a[0])==target_year: players_target_year[int(a[1])].add(int(a[3]))
	except EOFError:
		pass
	f.close()

#for e in ['team_rank.csv','team_rank_added.csv']:
#	f=codecs.open('team_rank.csv',mode='r',encoding='Shift-JIS')
#	f.close()
#年度,リーグID,チームID,試合,勝利,敗北,引分,勝率
#使わない方針

players_target_year[1]=list(players_target_year[1])
players_target_year[2]=list(players_target_year[2])
#open('submission.csv')
#リーグID-位置ID_順位,選手ID
for position in range(12):
	if position==7 or position==8 or position==9: continue
	for league in range(1,3):
		if league==1 and position==10: continue
		factors=[]
		for year in range(2009,target_year):
			y=year*league
			factors+=[position_rank_get(y,e[1],position)+batting_get(y,e[1])+pitching_get(y,e[1])+[e[3]] for e in train if e[0]==y and e[2]==position]
		target=[]
		for i in range(len(factors)): target.append(factors[i].pop())
		clf=LinearRegression()
		clf.fit(factors,target)
		factors=[position_rank_get(target_year*league,e,position)+batting_get(target_year*league,e)+pitching_get(target_year*league,e) for e in players_target_year[league]]
		predict=clf.predict(factors)
		result=sorted(zip(predict,players_target_year[league]),reverse=True)
		for i in range(20):
			print('%d-%d_%d,%d'%(league,position,i+1,result[i][1]))